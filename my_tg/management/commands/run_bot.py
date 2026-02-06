from django.core.management.base import BaseCommand
import sys
import logging
from my_tg.bot import setup_bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        self.stdout.write('Запуск Telegram бота...')

        try:
            bot_instance = setup_bot()
            if not bot_instance:
                self.stdout.write(self.style.ERROR('Не удалось настроить бота'))
                return

            # Проверяем тип бота (новая или старая версия API)
            try:
                from telegram.ext import Application
                is_new_api = isinstance(bot_instance, Application)
            except ImportError: # Если не можем импортировать Application, значит старая версия
                is_new_api = False

            if is_new_api:
                import asyncio

                if sys.platform == 'win32':
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                self.stdout.write('Используется новая версия API')

                try:
                    loop.run_until_complete(bot_instance.initialize())
                    loop.run_until_complete(bot_instance.start())
                    loop.run_until_complete(bot_instance.updater.start_polling())

                    self.stdout.write(self.style.SUCCESS('Бот запущен. Ctrl+C для остановки.'))

                    try:
                        loop.run_forever()
                    except KeyboardInterrupt:
                        self.stdout.write(self.style.WARNING('Остановка бота...'))
                    finally:
                        loop.run_until_complete(bot_instance.stop())
                        loop.run_until_complete(bot_instance.shutdown())
                        loop.close()

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))

            else:
                # Старая версия API
                from telegram.ext import Updater

                self.stdout.write('Используется старая версия API')

                bot_instance.start_polling()
                self.stdout.write(self.style.SUCCESS('Бот запущен. Ctrl+C для остановки.'))

                try:
                    bot_instance.idle()
                except KeyboardInterrupt:
                    self.stdout.write(self.style.WARNING('Остановка бота...'))
                finally:
                    bot_instance.stop()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
            logger.error(f"Ошибка запуска бота: {e}")