# Habit Tracker API

Бэкенд-часть SPA веб-приложения для трекера привычек, основанного на книге "Атомные привычки" Джеймса Клира.

## Функциональность

- 📝 Управление привычками (CRUD операции)
- 🔐 JWT аутентификация
- 📱 Интеграция с Telegram для напоминаний
- 🔄 Отложенные задачи через Celery
- 📊 Пагинация и фильтрация
- 📚 Документация API через Swagger/Redoc
- 🛡️ Настройки CORS для фронтенда

## Установка и запуск

### 1. Клонирование репозитория

```
git clone natalybalandina/Coursework-Django-REST-Framework
```

### 2. Настройка виртуального окружения
```
python -m venv venv
```
```
venv\Scripts\activate
```

### 3. Установка зависимостей
```
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
- Создан файл .env в корне проекта на основе .env.sample
- Создана базу данных в PostgreSQL
```
sudo -u postgres psql
CREATE DATABASE habittracker;
CREATE USER habittracker_user WITH PASSWORD 'habittracker_pass';
GRANT ALL PRIVILEGES ON DATABASE habittracker TO habittracker_user;
```

### 5. Применение миграций
```
python manage.py makemigrations
python manage.py migrate
```
### 6. Создан суперпользователm
```
python manage.py createsuperuser
```

### 7. Запуск Redis
** Для Windows (если установлен Redis):**
```
redis-server
```
### 8. Запуски
- сервера разработки
```
python manage.py runserver
```

- Celery worker
```
celery -A config worker -l info
```

- Celery beat (планировщик)
```
celery -A config beat -l info
```

- Telegram бот (опционально)
```
python manage.py run_bot
```

### 9. Настройка Telegram бота
1. Создание бота
Откройте Telegram и найдите @BotFather
Отправьте команду /newbot
Укажите имя бота (например, HabitTrackerBot)
Укажите username бота (например, habit_tracker_my_bot)
Сохраните токен, который выдаст BotFather
Добавьте токен в файл .env как TELEGRAM_BOT_TOKEN

2. Запуск бота
```
python manage.py run_bot
```
3. Привязка аккаунта
Найдите вашего бота в Telegram по username

*** Пример визуализации ***
*Привычки*
GET /api/habits/my/ - Список привычек текущего пользователя

POST /api/habits/my/ - Создание привычки

GET /api/habits/my/{id}/ - Получение привычки

PUT /api/habits/my/{id}/ - Обновление привычки

PATCH /api/habits/my/{id}/ - Частичное обновление привычки

DELETE /api/habits/my/{id}/ - Удаление привычки

GET /api/habits/public/ - Список публичных привычек


### Тестирование

1. Запуск тестов
```
python manage.py test
``

2. Покрытие тестами
``
pip install coverage
```

3. Запуск тестов с покрытием
```
coverage run --source='.' manage.py test
```
4. Генерация отчета
```
coverage report
```
Результаты тестов
```
Name                                                                Stmts   Miss  Cover
---------------------------------------------------------------------------------------
config\__init__.py                                                      2      0   100%
config\celery.py                                                        9      1    89%
config\settings.py                                                     36      0   100%
config\urls.py                                                          8      0   100%
habits\__init__.py                                                      0      0   100%
habits\admin.py                                                        12      0   100%
habits\apps.py                                                          5      0   100%
habits\migrations\0001_initial.py                                       9      0   100%
habits\migrations\0002_alter_habit_id_alter_habitcompletion_id.py       4      0   100%
habits\migrations\__init__.py                                           0      0   100%
habits\models.py                                                       37      0   100%
habits\permissions.py                                                  14      5    64%
habits\serializers.py                                                  19      1    95%
habits\tests.py                                                        85      3    96%
habits\urls.py                                                          6      0   100%
habits\validators.py                                                   33     10    70%
habits\views.py                                                        29      0   100%
manage.py                                                              11      2    82%
my_tg\__init__.py                                                       0      0   100%
my_tg\admin.py                                                          7      0   100%
my_tg\apps.py                                                           5      0   100%
my_tg\management\__init__.py                                            0      0   100%
my_tg\management\commands\__init__.py                                   0      0   100%
my_tg\migrations\0001_initial.py                                        7      0   100%
my_tg\migrations\0002_alter_telegramuser_user.py                        6      0   100%
my_tg\migrations\__init__.py                                            0      0   100%
my_tg\models.py                                                        13      0   100%
my_tg\tests.py                                                          1      0   100%
users\__init__.py                                                       0      0   100%
users\admin.py                                                          1      0   100%
users\apps.py                                                           5      0   100%
users\migrations\0001_initial.py                                        8      0   100%
users\migrations\0002_alter_user_id.py                                  4      0   100%
users\migrations\__init__.py                                            0      0   100%
users\models.py                                                         9      0   100%
users\tests.py                                                          1      0   100%
---------------------------------------------------------------------------------------
TOTAL                                                                 386     22    94%

```

### Документация

GET /swagger/ - Swagger документация

GET /redoc/ - ReDoc документация
