"""
Settings package for mysite project.

Импортирует настройки в зависимости от переменной окружения DJANGO_SETTINGS_MODULE.
По умолчанию используется dev.
"""

import os

# Определяем, какое окружение использовать
# Можно переопределить через переменную окружения DJANGO_SETTINGS_MODULE
# Например: export DJANGO_SETTINGS_MODULE=config.settings.prod

