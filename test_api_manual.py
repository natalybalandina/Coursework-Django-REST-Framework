import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
import requests

User = get_user_model()

# Создаем пользователя если нет
try:
    user = User.objects.get(username='testuser')
except User.DoesNotExist:
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

# Получаем токен
print("1. Получение токена...")
response = requests.post(
    'http://localhost:8000/api/token/',
    json={'username': 'testuser', 'password': 'testpass123'}
)

if response.status_code == 200:
    token = response.json()['access']
    print(f"   Токен получен")

    headers = {'Authorization': f'Bearer {token}'}

    print("\n2. Тестируем эндпоинты:")

    endpoints = [
        ('GET', '/api/habits/', 'Список привычек'),
        ('GET', '/api/habits/public/', 'Публичные привычки'),
        ('GET', '/api/public/', 'Публичные привычки (альтернативный)'),
    ]

    for method, endpoint, description in endpoints:
        print(f"\n   {description}:")
        print(f"   {method} {endpoint}")

        if method == 'GET':
            response = requests.get(f'http://localhost:8000{endpoint}', headers=headers)
        else:
            response = requests.post(f'http://localhost:8000{endpoint}', headers=headers)

        print(f"   Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                print(f"   ✓ Успешно! Найдено: {len(data['results'])} привычек")
            else:
                print(f"   ✓ Успешно! Данные: {data}")
        elif response.status_code == 404:
            print(f"   ✗ 404 - Не найдено")
        else:
            print(f"   ✗ Ошибка: {response.status_code}")
else:
    print(f"Ошибка получения токена: {response.status_code}")