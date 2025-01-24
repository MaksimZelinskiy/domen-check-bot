FROM python:3.12-slim

WORKDIR /app

# Установка необходимых зависимостей, включая postgresql-client
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Копирование и установка зависимостей
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY app/ .

# Делаем скрипт инициализации исполняемым
COPY app/init_db.sh .
RUN chmod +x init_db.sh

# Установка окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Запуск бота
CMD ["python", "main.py"]
