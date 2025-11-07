"""
Django staging settings for mysite project.

Настройки для staging сервера (тестовое окружение).
Максимально приближено к production, но с возможностью отладки.
"""

import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# Обязательно должен быть в переменных окружения!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY не установлен в переменных окружения!")

# DEBUG: В stage можно оставить True для отладки
# Но лучше постепенно переводить на False, чтобы быть ближе к prod
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Разрешенные хосты - только те, которые указаны в переменных окружения
ALLOWED_HOSTS = [
    host.strip() 
    for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') 
    if host.strip()
]

if not ALLOWED_HOSTS:
    raise ValueError("DJANGO_ALLOWED_HOSTS не установлен в переменных окружения!")


# Database
# PostgreSQL - как в production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 60,  # Переиспользование соединений (производительность)
    }
}


# Static files (CSS, JavaScript, Images)
# STATIC_ROOT - куда собираются файлы командой collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'

# STATICFILES_DIRS - откуда Django берёт статику ДО collectstatic
# Убираем эту настройку, если у тебя нет общей папки static/ в корне
# Если есть - раскомментируй:
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]


# Media files (uploads)
# На сервере медиа файлы должны быть в отдельной папке
MEDIA_ROOT = BASE_DIR / 'media'


# Security settings
# В stage можно ослабить некоторые настройки безопасности
SECURE_SSL_REDIRECT = False  # В stage может не быть SSL (но лучше настроить!)
SESSION_COOKIE_SECURE = False  # Требует HTTPS
CSRF_COOKIE_SECURE = False     # Требует HTTPS

# Эти настройки оставляем включенными
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


# Логирование в файл (для stage)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django-stage.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# Email backend для stage (можно настроить реальную отправку или консоль)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'