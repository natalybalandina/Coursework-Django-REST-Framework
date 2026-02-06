from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Telegram Chat ID'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
