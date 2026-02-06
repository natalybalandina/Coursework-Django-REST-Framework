from django.contrib import admin
from .models import Habit, HabitCompletion


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'place', 'time', 'is_pleasant', 'is_public')
    list_filter = ('is_pleasant', 'is_public', 'periodicity')
    search_fields = ('action', 'place', 'user__username')


@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'completed_at')
    list_filter = ('date',)
    search_fields = ('habit__action', 'notes')
