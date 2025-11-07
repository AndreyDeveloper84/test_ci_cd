"""
Django production settings for mysite project.

Настройки для production сервера.
Максимальная безопасность, DEBUG=False, все секреты из переменных окружения.
"""

import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# ОБЯЗАТЕЛЬНО должен быть в переменных окружения!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY не установлен в переменных окружения!")

# SECURITY WARNING: don't run with debug turned on in production!
# В production DEBUG ВСЕГДА должен быть False!
DEBUG = False

# Разрешенные хосты - только те, которые указаны в переменных окружения
ALLOWED_HOSTS = [
    host.strip() 
    for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') 
    if host.strip()
]

if not ALLOWED_HOSTS:
    raise ValueError("DJANGO_ALLOWED_HOSTS не установлен в переменных окружения!")


# Database
# PostgreSQL - надёжная production БД
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Переиспользование соединений (важно для производительности!)
        'OPTIONS': {
            'connect_timeout': 10,
        },
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
# На production сервере медиа файлы должны быть в безопасном месте
MEDIA_ROOT = BASE_DIR / 'media'


# Security settings
# В production все настройки безопасности на максимум!

# Перенаправлять HTTP на HTTPS (требует настройки SSL сертификата!)
SECURE_SSL_REDIRECT = True

# Cookies только через HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Дополнительная безопасность
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS - заставляет браузер использовать только HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Дополнительные настройки безопасности
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Логирование в файл (для production)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',  # В prod логируем только warnings и errors
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django-prod.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,  # Хранить 5 старых файлов
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# Email backend для production
# Настрой реальную отправку через SMTP (Gmail, SendGrid и т.д.)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')


# Кеширование (опционально, но очень полезно для производительности)
# Раскомментируй, если настроишь Redis на сервере:
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
#     }
# }