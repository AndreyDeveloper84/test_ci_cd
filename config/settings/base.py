"""
Django base settings for mysite project.

Базовые настройки, которые не меняются между окружениями.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR указывает на корень проекта (где manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Application definition
# Приложения Django, которые используются в проекте

INSTALLED_APPS = [
    # Встроенные приложения Django
    'django.contrib.admin',          # Админ-панель
    'django.contrib.auth',           # Система аутентификации
    'django.contrib.contenttypes',   # Система типов контента
    'django.contrib.sessions',       # Сессии
    'django.contrib.messages',       # Сообщения (flash messages)
    'django.contrib.staticfiles',    # Статические файлы (CSS, JS, изображения)
    
    # Здесь будут твои приложения, например:
    # 'blog',
    # 'accounts',
]

# Middleware - промежуточные слои обработки запросов
# Каждый запрос проходит через эти слои сверху вниз
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',       # Безопасность
    'django.contrib.sessions.middleware.SessionMiddleware',  # Сессии
    'django.middleware.common.CommonMiddleware',           # Общие функции
    'django.middleware.csrf.CsrfViewMiddleware',           # Защита от CSRF атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',  # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от clickjacking
]

# Главный файл с URL маршрутами
ROOT_URLCONF = 'config.urls'

# Настройки шаблонов (HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Добавил папку templates в корне
        'APP_DIRS': True,  # Искать шаблоны внутри приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI приложение для production
WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# Валидаторы паролей (проверяют сложность пароля)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# Настройки локализации

LANGUAGE_CODE = 'en-us'  # Язык по умолчанию

TIME_ZONE = 'UTC'  # Часовой пояс (можешь изменить на 'Europe/Moscow' например)

USE_I18N = True   # Включить интернационализацию

USE_TZ = True     # Использовать timezone-aware datetime


# Static files (CSS, JavaScript, Images)
# Настройки статических файлов

STATIC_URL = '/static/'  # URL для доступа к статике (например: /static/css/style.css)

# STATIC_ROOT - куда собираются все статические файлы для production
# Эта настройка переопределяется в stage.py и prod.py
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# Папки, где Django ищет статические файлы
# (помимо папок static/ внутри приложений)
# STATICFILES_DIRS будет настроен в dev.py, если нужна общая папка static/


# Media files (user uploads)
# Настройки загружаемых пользователями файлов

MEDIA_URL = '/media/'         # URL для доступа к медиа файлам
MEDIA_ROOT = BASE_DIR / 'media'  # Папка для хранения загруженных файлов


# Default primary key field type
# Тип первичного ключа по умолчанию для моделей
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'