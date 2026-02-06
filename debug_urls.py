import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver

resolver = get_resolver()

print("=" * 80)
print("ВСЕ ЗАРЕГИСТРИРОВАННЫЕ URL В ПРОЕКТЕ")
print("=" * 80)

def print_urls(url_patterns, prefix=''):
    for pattern in url_patterns:
        if hasattr(pattern, 'url_patterns'):
            # Это include
            print(f"{prefix}{pattern.pattern} -> INCLUDE")
            print_urls(pattern.url_patterns, prefix + '  ')
        elif hasattr(pattern, 'pattern'):
            # Обычный URL pattern
            name = getattr(pattern, 'name', 'Без имени')
            print(f"{prefix}{pattern.pattern} -> {name}")
        else:
            print(f"{prefix}Неизвестный pattern: {pattern}")

print_urls(resolver.url_patterns)

print("\n" + "=" * 80)
print("ПРОВЕРКА КОНКРЕТНЫХ URL")
print("=" * 80)

# Проверяем доступ к habits.urls
try:
    from django.urls import reverse
    print("1. Попытка reverse('habit-list'):")
    print(f"   Результат: {reverse('habit-list')}")
except Exception as e:
    print(f"   Ошибка: {e}")

try:
    print("\n2. Попытка reverse('public-habits'):")
    print(f"   Результат: {reverse('public-habits')}")
except Exception as e:
    print(f"   Ошибка: {e}")

print("\n" + "=" * 80)
print("ПРОВЕРКА ПУТЕЙ ВРУЧНУЮ")
print("=" * 80)

# Ручная проверка пути
test_paths = [
    '/api/',
    '/api/habits/',
    '/api/habits/public/',
    '/api/public/',
    '/api/token/',
]

for path in test_paths:
    try:
        match = resolver.resolve(path)
        print(f"✓ {path} -> {match}")
    except Exception as e:
        print(f"✗ {path} -> {e}")
