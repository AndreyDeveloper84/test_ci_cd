# Django Test CI/CD Project

Проект Django с настроенным CI/CD для автоматического деплоя на staging и production серверы.

## Структура проекта

```
.
├── mysite/                    # Основной проект Django
│   ├── config/               # Конфигурация проекта
│   │   ├── settings/         # Настройки для разных окружений
│   │   │   ├── base.py      # Базовые настройки
│   │   │   ├── dev.py       # Настройки для разработки
│   │   │   ├── stage.py     # Настройки для staging
│   │   │   └── prod.py      # Настройки для production
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── gunicorn_config.py   # Конфигурация Gunicorn
│   └── manage.py
├── scripts/                  # Скрипты для деплоя и настройки
│   ├── deploy.sh            # Скрипт деплоя
│   ├── setup-server.sh      # Скрипт настройки сервера
│   ├── mysite-stage.service # Systemd сервис для stage
│   ├── mysite-prod.service  # Systemd сервис для prod
│   ├── nginx-stage.conf     # Nginx конфиг для stage
│   └── nginx-prod.conf      # Nginx конфиг для prod
├── .github/
│   └── workflows/           # GitHub Actions workflows
│       ├── ci.yml           # CI pipeline
│       ├── deploy-stage.yml # Деплой на stage
│       └── deploy-prod.yml  # Деплой на production
├── requirements.txt         # Зависимости Python
├── .env.example            # Пример переменных окружения
└── CI_CD_PLAN.md           # Подробный план CI/CD

```

## Быстрый старт

### Локальная разработка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Скопируйте `.env.example` в `.env` и настройте переменные окружения
5. Примените миграции:
   ```bash
   cd mysite
   python manage.py migrate
   ```
6. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

## CI/CD

### Настройка GitHub Environments

1. Перейдите в Settings → Environments в вашем GitHub репозитории
2. Создайте два окружения: `stage` и `production`
3. Добавьте необходимые secrets (см. `CI_CD_PLAN.md`)

### Настройка сервера

1. Загрузите скрипты на сервер
2. Запустите `setup-server.sh` для первоначальной настройки:
   ```bash
   sudo bash scripts/setup-server.sh
   ```
3. Настройте базы данных PostgreSQL
4. Отредактируйте конфигурации Nginx (замените домены)
5. Настройте SSL сертификаты для production

### Workflow

- **CI**: Запускается при каждом push (тесты, линтинг)
- **Stage Deploy**: Запускается при push в ветку `develop` или `stage`
- **Production Deploy**: Запускается при push в ветку `main`/`master` или создании release tag

## Окружения

### Development (локально)
- Использует SQLite
- DEBUG = True
- Настройки: `config.settings.dev`

### Staging
- Использует PostgreSQL
- DEBUG = True (можно изменить на False)
- Настройки: `config.settings.stage`
- Деплой: push в `develop`/`stage`

### Production
- Использует PostgreSQL
- DEBUG = False
- Все настройки безопасности включены
- Деплой: push в `main`/`master` или release tag

## Дополнительная информация

Подробный план CI/CD и инструкции по настройке см. в файле `CI_CD_PLAN.md`.

