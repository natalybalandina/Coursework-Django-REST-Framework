from django.db import models
from django.conf import settings


class TelegramUser(models.Model):
    """Модель для хранения информации о Telegram пользователях"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='telegram_user'
    )

    chat_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Chat ID'
    )

    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Telegram username'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подключения'
    )

    class Meta:
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'

    def __str__(self):
        return f"{self.user.username} - {self.chat_id}"
