#!/bin/bash

# Скрипт для настройки сервера для деплоя Habit Tracker

set -e

echo "Настройка сервера для Habit Tracker..."

# Обновление системы
sudo apt-get update && sudo apt-get upgrade -y

# Установка Docker
if ! command -v docker &> /dev/null; then
    echo "Установка Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

# Установка Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Установка Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Создание директории для проекта
sudo mkdir -p /opt/habittracker
sudo chown $USER:$USER /opt/habittracker

# Копирование файлов проекта
cp docker-compose.yml /opt/habittracker/
cp -r nginx /opt/habittracker/

echo "Сервер настроен успешно!"
echo "Следующие шаги:"
echo "1. Скопируйте .env файл в /opt/habittracker/"
echo "2. Запустите docker-compose up -d"