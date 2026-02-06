import logging
import asyncio
import sys
from django.conf import settings

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters
    from telegram.error import TelegramError
    NEW_API = True
except ImportError:
    try:
        from telegram import Update
        from telegram.ext import Updater, CommandHandler, CallbackContext
        NEW_API = False
    except ImportError:
        raise ImportError("python-telegram-bot не установлен. Установите: pip install python-telegram-bot")

logger = logging.getLogger(__name__)


async def start_command(update, context):
    """Обработчик команды /start"""
    try:
        user = update.effective_user
        chat_id = update.effective_chat.id

        logger.info(f"Получена команда /start от пользователя {user.username} (chat_id: {chat_id})")

        import uuid
        connection_code = str(uuid.uuid4())[:8]

        await update.message.reply_text(
            f"Привет, {user.first_name}!\n\n"
            f"Добро пожаловать в Habit Tracker Bot!\n\n"
            f"Ваш код для привязки аккаунта: `{connection_code}`\n\n"
            f"Чтобы привязать аккаунт:\n"
            f"1. Перейдите в личный кабинет на сайте\n"
            f"2. Введите этот код в разделе 'Настройки Telegram'\n\n"
            f"Или используйте команду:\n"
            f"`/connect {connection_code}`"
        )

    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")


async def connect_command(update, context):
    """Обработчик команды /connect"""
    try:
        args = context.args
        chat_id = update.effective_chat.id

        if not args:
            await update.message.reply_text(
                "Не указан код подключения.\n"
                "Использование: `/connect <ваш_код>`"
            )
            return

        code = args[0].strip()

        await update.message.reply_text(
            f"Код подключения получен: {code}\n\n"
            f"Ваш Chat ID: `{chat_id}`\n"
            f"Сохраните эту информацию для настройки уведомлений."
        )

    except Exception as e:
        logger.error(f"Ошибка в команде /connect: {e}")


async def help_command(update, context):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "Доступные команды:\n\n"
        "`/start` - Начать работу, получить код привязки\n"
        "`/connect <код>` - Привязать аккаунт\n"
        "`/help` - Показать справку"
    )


async def send_reminder_async(chat_id: int, message: str):
    """Асинхронная отправка напоминания"""
    try:
        token = settings.TELEGRAM_BOT_TOKEN
        if not token:
            logger.error("TELEGRAM_BOT_TOKEN не настроен!")
            return False

        application = Application.builder().token(token).build()
        await application.initialize()
        await application.start()

        try:
            await application.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logger.info(f"Напоминание отправлено пользователю {chat_id}")
            return True
        finally:
            await application.stop()
            await application.shutdown()

    except Exception as e:
        logger.error(f"Ошибка отправки напоминания пользователю {chat_id}: {e}")
        return False


def send_reminder_sync(chat_id: int, message: str) -> bool:
    """Синхронная обертка для отправки напоминания"""
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(send_reminder_async(chat_id, message))
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Ошибка в синхронной отправке: {e}")
        return False


def setup_bot():
    """Настройка бота"""
    token = settings.TELEGRAM_BOT_TOKEN

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не настроен!")
        return None

    try:
        # Создаем приложение
        application = Application.builder().token(token).build()

        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("connect", connect_command))
        application.add_handler(CommandHandler("help", help_command))

        # Обработчик для неизвестных команд
        async def unknown_command(update, context):
            await update.message.reply_text("Неизвестная команда. Используйте /help.")

        application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

        logger.info("Telegram бот успешно настроен")
        return application

    except Exception as e:
        logger.error(f"Ошибка настройки Telegram бота: {e}")
        return None
