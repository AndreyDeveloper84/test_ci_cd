#!/bin/bash

# Скрипт деплоя Django приложения на сервер
# Использование: ./deploy.sh [stage|prod]

set -e  # Остановить выполнение при ошибке

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
    echo "❌ Ошибка: Не указано окружение (stage или prod)"
    echo "Использование: ./deploy.sh [stage|prod]"
    exit 1
fi

if [ "$ENVIRONMENT" != "stage" ] && [ "$ENVIRONMENT" != "prod" ]; then
    echo "❌ Ошибка: Окружение должно быть 'stage' или 'prod'"
    exit 1
fi

echo "🚀 Начало деплоя в окружение: $ENVIRONMENT"
echo "📅 Дата: $(date '+%Y-%m-%d %H:%M:%S')"

# Определяем настройки в зависимости от окружения
if [ "$ENVIRONMENT" == "stage" ]; then
    SETTINGS_MODULE="config.settings.stage"
    SERVICE_NAME="mysite-stage"
else
    SETTINGS_MODULE="config.settings.prod"
    SERVICE_NAME="mysite-prod"
fi

echo "⚙️  Настройки:"
echo "  - Окружение: $ENVIRONMENT"
echo "  - Settings module: $SETTINGS_MODULE"
echo "  - Service name: $SERVICE_NAME"
echo "  - Deploy path: $DEPLOY_PATH"

# Создаем временный файл с переменными окружения
ENV_FILE=$(mktemp)
cat > "$ENV_FILE" <<EOF
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
DJANGO_SECRET_KEY='${DJANGO_SECRET_KEY}'
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD='${DB_PASSWORD}'
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DJANGO_ALLOWED_HOSTS='${DJANGO_ALLOWED_HOSTS}'
EOF

echo "📦 Создание архива проекта..."

# Создаем архив проекта (исключая ненужные файлы)
tar --exclude='.git' \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.pyo' \
    --exclude='db.sqlite3' \
    --exclude='.env' \
    --exclude='staticfiles' \
    --exclude='media' \
    --exclude='logs' \
    --exclude='*.log' \
    --exclude='.pytest_cache' \
    --exclude='htmlcov' \
    --exclude='backups' \
    -czf /tmp/mysite-deploy.tar.gz .

echo "📤 Копирование файлов на сервер..."

# Копируем архив на сервер
scp -P "$SSH_PORT" /tmp/mysite-deploy.tar.gz "$SSH_USER@$SSH_HOST:/tmp/"

# Копируем файл с переменными окружения
scp -P "$SSH_PORT" "$ENV_FILE" "$SSH_USER@$SSH_HOST:/tmp/.env.deploy"

echo "🔧 Выполнение команд на сервере..."

# Выполняем команды на сервере
ssh "$SSH_USER@$SSH_HOST" bash -s "$DEPLOY_PATH" "$ENVIRONMENT" "$SERVICE_NAME" <<'ENDSSH'
set -e
DEPLOY_PATH="$1"
ENVIRONMENT="$2"
SERVICE_NAME="$3"
DJANGO_SETTINGS_MODULE="$4"

echo "📂 Рабочая директория: $DEPLOY_PATH"
cd "$DEPLOY_PATH" || exit 1

echo "📂 Переход в директорию проекта..."
cd "$DEPLOY_PATH" || { echo "❌ Директория $DEPLOY_PATH не существует!"; exit 1; }

# Проверяем что мы в правильной директории
echo "   Текущая директория: $(pwd)"
ls -la | head -10

echo "💾 Создание резервной копии..."
BACKUP_DIR="backups/backup_$(date +%Y%m%d_%H%M%S)"
if [ -d "mysite" ]; then
    mkdir -p backups
    echo "  - Копирование текущей версии в $BACKUP_DIR"
    cp -r mysite "$BACKUP_DIR" || echo "⚠️  Не удалось создать бэкап, продолжаем..."
fi

echo "🗑️  Удаление старого кода..."
rm -rf mysite

echo "📦 Распаковка нового кода..."
mkdir -p mysite
tar -xzf /tmp/mysite-deploy.tar.gz -C mysite/
rm /tmp/mysite-deploy.tar.gz

echo "🐍 Настройка виртуального окружения..."
if [ ! -d ".venv" ]; then
    echo "  - Создание нового virtualenv с Python 3.12"
    python3.12 -m venv .venv
fi
source .venv/bin/activate

echo "  - Python version: $(python --version)"
echo "  - Pip version: $(pip --version)"

echo "📥 Установка зависимостей..."
pip install --upgrade pip --quiet
pip install -r mysite/requirements.txt --quiet

echo "⚙️  Настройка переменных окружения..."
cp /tmp/.env.deploy .env
chmod 600 .env
rm /tmp/.env.deploy

echo "  - Загрузка переменных окружения..."
set -a  # Автоматический export всех переменных
source .env
set +a

echo "📁 Создание необходимых директорий..."
mkdir -p logs
mkdir -p staticfiles
mkdir -p media

echo "🔄 Применение миграций базы данных..."
echo "Выведем содержание deploy path"
echo "$DEPLOY_PATH"
cd "$DEPLOY_PATH" || exit 1
source .venv/bin/activate
python manage.py migrate --noinput

echo "📦 Сбор статических файлов..."
cd "$DEPLOY_PATH" || exit 1
source .venv/bin/activate
python manage.py collectstatic --noinput --clear

echo "🔍 Проверка конфигурации Django..."
python manage.py check --deploy || echo "⚠️  Есть предупреждения в конфигурации"

cd ..

echo "🔄 Перезапуск сервиса..."
if systemctl list-unit-files | grep -q "$SERVICE_NAME.service"; then
    cd "$DEPLOY_PATH" || exit 1
    sudo systemctl restart "$SERVICE_NAME"
    echo "  - Сервис $SERVICE_NAME перезапущен"
    
    # Ждём 3 секунды для запуска
    sleep 3
    
    # Проверка статуса
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo "✅ Сервис $SERVICE_NAME работает"
    else
        echo "❌ Сервис $SERVICE_NAME не запустился!"
        echo "Логи сервиса:"
        sudo journalctl -u "$SERVICE_NAME" -n 20 --no-pager
        exit 1
    fi
else
    echo "⚠️  Сервис $SERVICE_NAME не настроен"
    echo "⚠️  Запустите gunicorn вручную или создайте systemd service"
fi

echo ""
echo "✅ Деплой завершен успешно!"
echo "📊 Статистика:"
echo "  - Окружение: $ENVIRONMENT"
echo "  - Путь: $DEPLOY_PATH"
echo "  - Время: $(date '+%Y-%m-%d %H:%M:%S')"

ENDSSH

# Удаляем временные файлы
rm -f /tmp/mysite-deploy.tar.gz "$ENV_FILE"

echo ""
echo "🎉 Деплой завершен!"
echo ""
