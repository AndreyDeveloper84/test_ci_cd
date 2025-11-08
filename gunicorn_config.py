"""
Конфигурация Gunicorn для Django проекта
"""

import multiprocessing
import os

# Базовый путь к проекту
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Количество воркеров
workers = multiprocessing.cpu_count() * 2 + 1

# Биндинг
bind = "127.0.0.1:8000"

# Пользователь и группа (раскомментируйте и настройте при необходимости)
# user = "deploy"
# group = "deploy"

# Логирование
logs_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)
accesslog = os.path.join(logs_dir, "gunicorn_access.log")
errorlog = os.path.join(logs_dir, "gunicorn_error.log")
loglevel = "info"

# Процессы
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Перезапуск
max_requests = 1000
max_requests_jitter = 50

# Безопасность
limit_request_line = 4094
limit_request_fields = 100

# Имя приложения
wsgi_app = "config.wsgi:application"

# Предзагрузка приложения
preload_app = True

# Перезапуск при изменении кода (только для разработки)
reload = False

