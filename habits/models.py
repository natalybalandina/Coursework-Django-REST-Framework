from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Habit(models.Model):
    """Модель привычки"""

    DAILY = 1
    WEEKLY = 7

    PERIODICITY_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения'
    )

    time = models.TimeField(
        verbose_name='Время выполнения'
    )

    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка'
    )

    periodicity = models.PositiveIntegerField(
        choices=PERIODICITY_CHOICES,
        default=DAILY,
        verbose_name='Периодичность',
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )

    estimated_time = models.PositiveIntegerField(
        verbose_name='Время на выполнение (в секундах)',
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}: {self.action}"


class HabitCompletion(models.Model):
    """Модель для отслеживания выполнения привычек"""
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='completions',
        verbose_name='Привычка'
    )

    date = models.DateField(
        verbose_name='Дата выполнения',
        default=timezone.now
    )

    completed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время отметки'
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Заметки'
    )

    class Meta:
        verbose_name = 'Выполнение привычки'
        verbose_name_plural = 'Выполнения привычек'
        unique_together = ['habit', 'date']

    def __str__(self):
        return f"{self.habit.action} - {self.date}"
