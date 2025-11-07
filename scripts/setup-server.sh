#!/bin/bash

# Скрипт первоначальной настройки сервера для Django проекта
# Запускать с правами root или через sudo

set -e

echo "🔧 Начало настройки сервера для Django проекта"

# Обновление системы
echo "📦 Обновление системы..."
apt-get update
apt-get upgrade -y

# Установка системных зависимостей
echo "📥 Установка системных зависимостей..."
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    curl \
    supervisor \
    certbot \
    python3-certbot-nginx

# Создание пользователя для деплоя
echo "👤 Создание пользователя deploy..."
if ! id "deploy" &>/dev/null; then
    useradd -m -s /bin/bash deploy
    usermod -aG www-data deploy
    echo "✅ Пользователь deploy создан"
else
    echo "ℹ️  Пользователь deploy уже существует"
fi

# Создание директорий
echo "📂 Создание директорий..."
mkdir -p /var/www/mysite-stage
mkdir -p /var/www/mysite-prod
mkdir -p /var/www/mysite-stage/backups
mkdir -p /var/www/mysite-prod/backups
mkdir -p /var/www/mysite-stage/mysite/logs
mkdir -p /var/www/mysite-prod/mysite/logs

# Установка прав
chown -R deploy:www-data /var/www/mysite-stage
chown -R deploy:www-data /var/www/mysite-prod
chmod -R 755 /var/www/mysite-stage
chmod -R 755 /var/www/mysite-prod

# Настройка PostgreSQL
echo "🗄️  Настройка PostgreSQL..."
echo "⚠️  ВАЖНО: Необходимо вручную создать базы данных и пользователей!"
echo "Выполните следующие команды:"
echo ""
echo "sudo -u postgres psql"
echo "CREATE DATABASE mysite_stage_db;"
echo "CREATE DATABASE mysite_prod_db;"
echo "CREATE USER mysite_stage_user WITH PASSWORD 'your_password_here';"
echo "CREATE USER mysite_prod_user WITH PASSWORD 'your_password_here';"
echo "GRANT ALL PRIVILEGES ON DATABASE mysite_stage_db TO mysite_stage_user;"
echo "GRANT ALL PRIVILEGES ON DATABASE mysite_prod_db TO mysite_prod_user;"
echo "\\q"

# Копирование systemd сервисов
echo "⚙️  Настройка systemd сервисов..."
if [ -f "mysite-stage.service" ]; then
    cp mysite-stage.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable mysite-stage.service
    echo "✅ Сервис mysite-stage настроен"
fi

if [ -f "mysite-prod.service" ]; then
    cp mysite-prod.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable mysite-prod.service
    echo "✅ Сервис mysite-prod настроен"
fi

# Настройка Nginx
echo "🌐 Настройка Nginx..."
if [ -f "nginx-stage.conf" ]; then
    cp nginx-stage.conf /etc/nginx/sites-available/mysite-stage
    ln -sf /etc/nginx/sites-available/mysite-stage /etc/nginx/sites-enabled/
    echo "✅ Конфигурация Nginx для stage создана"
fi

if [ -f "nginx-prod.conf" ]; then
    cp nginx-prod.conf /etc/nginx/sites-available/mysite-prod
    ln -sf /etc/nginx/sites-available/mysite-prod /etc/nginx/sites-enabled/
    echo "✅ Конфигурация Nginx для prod создана"
fi

# Проверка конфигурации Nginx
nginx -t

echo ""
echo "✅ Настройка сервера завершена!"
echo ""
echo "📝 Следующие шаги:"
echo "1. Настройте базы данных PostgreSQL (см. инструкции выше)"
echo "2. Отредактируйте конфигурации Nginx (замените домены)"
echo "3. Настройте SSL сертификаты для production (certbot)"
echo "4. Перезапустите Nginx: sudo systemctl restart nginx"
echo "5. Настройте SSH ключи для GitHub Actions"

