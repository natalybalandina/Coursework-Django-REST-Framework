from rest_framework import serializers


class HabitValidator:
    """Валидатор для привычек"""

    @staticmethod
    def validate_related_habit_and_reward(data):
        """Исключить одновременный выбор связанной привычки и указания вознаграждения"""
        related_habit = data.get('related_habit')
        reward = data.get('reward')

        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать связанную привычку и вознаграждение"
            )
        return data

    @staticmethod
    def validate_estimated_time(value):
        """Время выполнения должно быть не больше 120 секунд"""
        if value > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд"
            )
        return value

    @staticmethod
    def validate_related_habit(value):
        """В связанные привычки могут попадать только привычки с признаком приятной привычки"""
        if value and not value.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной"
            )
        return value

    @staticmethod
    def validate_pleasant_habit(data):
        """У приятной привычки не может быть вознаграждения или связанной привычки"""
        is_pleasant = data.get('is_pleasant', False)

        if is_pleasant:
            if data.get('reward'):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть вознаграждения"
                )
            if data.get('related_habit'):
                raise serializers.ValidationError(
                    "У приятной привычки не может быть связанной привычки"
                )
        return data

    @staticmethod
    def validate_periodicity(value):
        """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
        if value > 7:
            raise serializers.ValidationError(
                "Периодичность не может быть больше 7 дней"
            )
        return value
    