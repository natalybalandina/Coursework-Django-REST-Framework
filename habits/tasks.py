from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from habits.models import Habit, HabitCompletion
from my_tg.bot import send_reminder_sync
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках"""
    now = timezone.localtime(timezone.now())
    current_time = now.time()

    # Находим привычки, которые нужно выполнить в это время
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    ).select_related('user')

    sent_count = 0

    for habit in habits:
        try:
            # Проверяем, есть ли у пользователя привязанный Telegram
            if hasattr(habit.user, 'telegram') and habit.user.telegram.is_active:

                # Формируем сообщение с эмодзи
                emoji = "🌟" if habit.is_pleasant else "✅"
                message = (
                    f"{emoji} *Напоминание о привычке!*\n\n"
                    f"*Действие:* {habit.action}\n"
                    f"*Место:* {habit.place}\n"
                    f"*Время на выполнение:* {habit.estimated_time} секунд\n"
                )

                if habit.reward:
                    message += f"*Вознаграждение:* {habit.reward}\n"

                if habit.related_habit:
                    message += f"*После этого:* {habit.related_habit.action}\n"

                message += f"\n_Не забудьте отметить выполнение в приложении!_"

                # Отправляем напоминание
                success = send_reminder_sync(
                    habit.user.telegram.chat_id,
                    message
                )

                if success:
                    sent_count += 1
                    logger.info(f"Напоминание отправлено для привычки: {habit.action}")
                else:
                    logger.error(f"Не удалось отправить напоминание для привычки: {habit.action}")

        except Exception as e:
            logger.error(f"Ошибка обработки привычки {habit.id}: {e}")
            continue

    logger.info(f"Отправлено {sent_count} напоминаний из {habits.count()} привычек")
    return f"Отправлено {sent_count} напоминаний"


@shared_task
def check_daily_habits():
    """Проверка ежедневных привычек"""
    today = timezone.localdate()
    users_with_telegram = User.objects.filter(
        telegram__isnull=False,
        telegram__is_active=True
    )

    for user in users_with_telegram:
        try:
            # Получаем привычки пользователя
            habits = Habit.objects.filter(user=user, periodicity=1)

            for habit in habits:
                # Проверяем, выполнена ли привычка сегодня
                completed_today = HabitCompletion.objects.filter(
                    habit=habit,
                    date=today
                ).exists()

                if not completed_today:
                    # Отправляем вечернее напоминание
                    message = (
                        f"🌙 *Вечернее напоминание*\n\n"
                        f"Вы еще не выполнили привычку:\n"
                        f"*{habit.action}*\n\n"
                        f"Не забудьте отметить выполнение!"
                    )

                    send_reminder_sync(user.telegram.chat_id, message)

        except Exception as e:
            logger.error(f"Ошибка проверки привычек пользователя {user.username}: {e}")
            continue
