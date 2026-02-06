from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger(__name__)


class HabitPagination(PageNumberPagination):
    """Пагинация для привычек"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для привычек пользователя"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = HabitPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        """Получение только привычек текущего пользователя"""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Сохранение пользователя при создании привычки"""
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        """Получение только публичных привычек"""
        return Habit.objects.filter(is_public=True)
