"""
Django development settings for mysite project.

Настройки для локальной разработки.
Здесь DEBUG=True, используется SQLite, все просто и удобно для разработки.
"""

import os
from .base import *

# Можно загружать переменные из .env файла (но для dev это не обязательно)
# Если создашь .env файл локально, то переменные будут браться оттуда

# SECURITY WARNING: keep the secret key used in production secret!
# Для разработки можно использовать любой ключ
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-em=$cf$0hws&6(+-dxbrl7b1e(lg-o$f+fd!@10=*38fy7z25r'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# В dev режиме разрешаем доступ со всех хостов
ALLOWED_HOSTS = ['*']


# Database
# Для разработки используем SQLite (файловая БД, не требует установки)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Static files
# В dev режиме статика раздаётся автоматически через runserver
# Если хочешь общую папку static/ в корне проекта:
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]


# Email backend для разработки (письма выводятся в консоль)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Логирование в консоль (удобно для отладки)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}