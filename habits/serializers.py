from rest_framework import serializers
from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычек"""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate(self, data):
        """Применение всех валидаторов"""
        validator = HabitValidator()

        # Проверка связанной привычки и вознаграждения
        data = validator.validate_related_habit_and_reward(data)

        # Проверка времени выполнения
        if 'estimated_time' in data:
            validator.validate_estimated_time(data['estimated_time'])

        # Проверка связанной привычки
        if 'related_habit' in data and data['related_habit']:
            validator.validate_related_habit(data['related_habit'])

        # Проверка приятной привычки
        data = validator.validate_pleasant_habit(data)

        # Проверка периодичности
        if 'periodicity' in data:
            validator.validate_periodicity(data['periodicity'])

        return data
