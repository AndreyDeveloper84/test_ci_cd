# План настройки CI/CD для Django проекта

## Архитектура

### Окружения:
1. **Local (локальная разработка)** - на вашем компьютере
2. **Stage (staging)** - тестовый сервер, максимально приближенный к production
3. **Production** - боевой сервер

### Структура на сервере:
```
/var/www/
├── mysite-stage/      # Staging окружение
│   ├── mysite/        # Код проекта
│   ├── .venv/         # Виртуальное окружение
│   ├── staticfiles/   # Статические файлы
│   └── .env           # Переменные окружения для stage
│
└── mysite-prod/       # Production окружение
    ├── mysite/        # Код проекта
    ├── .venv/         # Виртуальное окружение
    ├── staticfiles/   # Статические файлы
    └── .env           # Переменные окружения для prod
```

## Workflow CI/CD

### 1. CI (Continuous Integration) - автоматические проверки

**Триггер:** Push в любую ветку

**Шаги:**
- ✅ Установка зависимостей
- ✅ Линтинг кода (flake8, black, isort)
- ✅ Запуск тестов
- ✅ Проверка миграций Django
- ✅ Проверка безопасности (safety, bandit)

### 2. CD для Stage

**Триггер:** Push в ветку `develop` или `stage`

**Шаги:**
- ✅ Запуск всех проверок из CI
- ✅ Сборка проекта
- ✅ Деплой на staging сервер
- ✅ Запуск миграций
- ✅ Сбор статических файлов
- ✅ Перезапуск сервиса (systemd/gunicorn)

### 3. CD для Production

**Триггер:** Push в ветку `main` или `master`, или создание release tag

**Шаги:**
- ✅ Запуск всех проверок из CI
- ✅ Сборка проекта
- ✅ Деплой на production сервер
- ✅ Запуск миграций
- ✅ Сбор статических файлов
- ✅ Перезапуск сервиса
- ✅ Health check

## Необходимые Secrets в GitHub Environments

### Environment: `stage`

1. **SSH_HOST** - IP адрес или домен staging сервера
2. **SSH_USER** - пользователь для SSH подключения
3. **SSH_PRIVATE_KEY** - приватный SSH ключ для подключения к серверу
4. **SSH_PORT** - порт SSH (обычно 22)
5. **DEPLOY_PATH_STAGE** - путь к папке на сервере (например: `/var/www/mysite-stage`)
6. **DJANGO_SECRET_KEY_STAGE** - секретный ключ Django для stage
7. **DB_NAME_STAGE** - имя базы данных для stage
8. **DB_USER_STAGE** - пользователь базы данных для stage
9. **DB_PASSWORD_STAGE** - пароль базы данных для stage
10. **DB_HOST_STAGE** - хост базы данных для stage
11. **DB_PORT_STAGE** - порт базы данных для stage (обычно 5432)
12. **DJANGO_ALLOWED_HOSTS_STAGE** - разрешенные хосты для stage (через запятую)

### Environment: `production`

1. **SSH_HOST** - IP адрес или домен production сервера
2. **SSH_USER** - пользователь для SSH подключения
3. **SSH_PRIVATE_KEY** - приватный SSH ключ для подключения к серверу
4. **SSH_PORT** - порт SSH (обычно 22)
5. **DEPLOY_PATH_PROD** - путь к папке на сервере (например: `/var/www/mysite-prod`)
6. **DJANGO_SECRET_KEY_PROD** - секретный ключ Django для production
7. **DB_NAME_PROD** - имя базы данных для production
8. **DB_USER_PROD** - пользователь базы данных для production
9. **DB_PASSWORD_PROD** - пароль базы данных для production
10. **DB_HOST_PROD** - хост базы данных для production
11. **DB_PORT_PROD** - порт базы данных для production (обычно 5432)
12. **DJANGO_ALLOWED_HOSTS_PROD** - разрешенные хосты для production (через запятую)

## Необходимые доступы и настройки на сервере

### 1. SSH доступ
- ✅ Настроить SSH ключ для GitHub Actions
- ✅ Пользователь должен иметь права на запись в папки проекта
- ✅ Рекомендуется создать отдельного пользователя для деплоя (например: `deploy`)

### 2. Системные зависимости на сервере
- ✅ Python 3.11+ 
- ✅ PostgreSQL (для stage и prod)
- ✅ Nginx (для раздачи статики и проксирования)
- ✅ Gunicorn или uWSGI (WSGI сервер)
- ✅ Systemd (для управления сервисами)

### 3. Структура папок на сервере
```bash
# Создать папки
sudo mkdir -p /var/www/mysite-stage
sudo mkdir -p /var/www/mysite-prod
sudo chown -R deploy:deploy /var/www/mysite-stage
sudo chown -R deploy:deploy /var/www/mysite-prod
```

### 4. Systemd сервисы
Нужно создать два systemd сервиса:
- `mysite-stage.service` - для staging
- `mysite-prod.service` - для production

### 5. Nginx конфигурация
Нужны два конфига:
- `/etc/nginx/sites-available/mysite-stage` - для staging
- `/etc/nginx/sites-available/mysite-prod` - для production

### 6. Базы данных
- ✅ Создать отдельные базы данных для st   age и prod
- ✅ Создать пользователей БД с соответствующими правами

## Файлы, которые нужно создать

1. ✅ `.github/workflows/ci.yml` - CI pipeline
2. ✅ `.github/workflows/deploy-stage.yml` - Деплой на stage
3. ✅ `.github/workflows/deploy-prod.yml` - Деплой на production
4. ✅ `scripts/deploy.sh` - Скрипт деплоя
5. ✅ `scripts/setup-server.sh` - Скрипт первоначальной настройки сервера
6. ✅ `gunicorn_config.py` - Конфигурация Gunicorn
7. ✅ `.env.example` - Пример файла с переменными окружения
8. ✅ `.gitignore` - Игнорирование ненужных файлов

## Порядок действий

### Шаг 1: Подготовка проекта
- [x] Создать settings/stage.py
- [x] Создать requirements.txt
- [ ] Добавить тесты (если их нет)
- [ ] Добавить линтеры в requirements.txt

### Шаг 2: Настройка GitHub
- [ ] Создать репозиторий (если еще не создан)
- [ ] Настроить Environments в GitHub (Settings → Environments)
- [ ] Добавить все необходимые Secrets в каждое окружение

### Шаг 3: Настройка сервера
- [ ] Установить системные зависимости
- [ ] Создать пользователя для деплоя
- [ ] Настроить SSH ключи
- [ ] Создать папки для проектов
- [ ] Настроить PostgreSQL
- [ ] Настроить Nginx
- [ ] Создать systemd сервисы

### Шаг 4: Создание CI/CD файлов
- [ ] Создать GitHub Actions workflows
- [ ] Создать скрипты деплоя
- [ ] Протестировать деплой на stage

### Шаг 5: Тестирование
- [ ] Протестировать CI pipeline
- [ ] Протестировать деплой на stage
- [ ] Протестировать деплой на production

## Ветки Git

Рекомендуемая структура веток:
- `main` / `master` - production код
- `develop` / `stage` - staging код
- `feature/*` - ветки для разработки новых функций

## Защита веток

Рекомендуется настроить в GitHub:
- `main` - требует Pull Request и ревью перед мерджем
- `develop` - может быть защищена или нет (на ваше усмотрение)

