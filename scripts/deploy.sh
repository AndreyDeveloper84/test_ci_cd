#!/bin/bash

# Скрипт деплоя Django приложения на сервер
# Использование: ./deploy.sh [stage|prod]

set -e  # Остановить выполнение при ошибке

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
    echo "Ошибка: Не указано окружение (stage или prod)"
    exit 1
fi

if [ "$ENVIRONMENT" != "stage" ] && [ "$ENVIRONMENT" != "prod" ]; then
    echo "Ошибка: Окружение должно быть 'stage' или 'prod'"
    exit 1
fi

echo "🚀 Начало деплоя в окружение: $ENVIRONMENT"

# Определяем настройки в зависимости от окружения
if [ "$ENVIRONMENT" == "stage" ]; then
    SETTINGS_MODULE="config.settings.stage"
    SERVICE_NAME="mysite-stage"
else
    SETTINGS_MODULE="config.settings.prod"
    SERVICE_NAME="mysite-prod"
fi

# Создаем временный файл с переменными окружения
ENV_FILE=$(mktemp)
cat > "$ENV_FILE" <<EOF
DJANGO_SETTINGS_MODULE=$SETTINGS_MODULE
DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS
EOF

echo "📦 Копирование файлов на сервер..."

# Создаем архив проекта (исключая ненужные файлы)
tar --exclude='.git' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='db.sqlite3' \
    --exclude='.env' \
    --exclude='staticfiles' \
    -czf /tmp/mysite-deploy.tar.gz .

# Копируем архив на сервер
scp -P "$SSH_PORT" /tmp/mysite-deploy.tar.gz "$SSH_USER@$SSH_HOST:/tmp/"

# Копируем файл с переменными окружения
scp -P "$SSH_PORT" "$ENV_FILE" "$SSH_USER@$SSH_HOST:/tmp/.env"

# Выполняем команды на сервере
ssh -p "$SSH_PORT" "$SSH_USER@$SSH_HOST" <<ENDSSH
set -e

echo "📂 Переход в директорию проекта..."
cd $DEPLOY_PATH

echo "💾 Создание резервной копии..."
if [ -d "mysite" ]; then
    BACKUP_DIR="backup_\$(date +%Y%m%d_%H%M%S)"
    mkdir -p backups
    cp -r mysite "backups/\$BACKUP_DIR" || true
fi

echo "📦 Распаковка нового кода..."
mkdir -p mysite
cd mysite
tar -xzf /tmp/mysite-deploy.tar.gz
rm /tmp/mysite-deploy.tar.gz

echo "🐍 Активация виртуального окружения..."
if [ ! -d "../.venv" ]; then
    python3 -m venv ../.venv
fi
source ../.venv/bin/activate

echo "📥 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

echo "⚙️  Настройка переменных окружения..."
cp /tmp/.env .env
chmod 600 .env
rm /tmp/.env

echo "🔄 Применение миграций..."
export \$(cat .env | xargs)
cd mysite
python manage.py migrate --noinput

echo "📦 Сбор статических файлов..."
python manage.py collectstatic --noinput --clear

echo "🔄 Перезапуск сервиса..."
sudo systemctl restart $SERVICE_NAME || echo "⚠️  Сервис $SERVICE_NAME не найден, пропускаем перезапуск"

echo "✅ Деплой завершен успешно!"

# Проверка статуса сервиса
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "✅ Сервис $SERVICE_NAME работает"
else
    echo "⚠️  Сервис $SERVICE_NAME не запущен"
fi

ENDSSH

# Удаляем временные файлы
rm -f /tmp/mysite-deploy.tar.gz "$ENV_FILE"

echo "🎉 Деплой завершен!"

