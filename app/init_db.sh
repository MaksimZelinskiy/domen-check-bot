#!/bin/bash

# Добавляем небольшую задержку для уверенности, что PostgreSQL полностью запустился
sleep 5

echo "Starting database initialization..."
echo "Using connection parameters:"
echo "DB_HOST: $DB_HOST"
echo "DB_USER: postgres"  # Сначала подключаемся как postgres
echo "DB_NAME: postgres"  # Сначала к базе postgres

# Пробуем подключиться к postgres базе как postgres пользователь
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U postgres -d postgres -c '\l' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up - executing commands"

# Создаем пользователя, если он не существует
echo "Creating user $DB_USER if not exists..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U postgres -d postgres -c "DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$DB_USER') THEN
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
  END IF;
END
\$\$;"

# Даем пользователю права суперпользователя
echo "Granting privileges to $DB_USER..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U postgres -d postgres -c "ALTER USER $DB_USER WITH SUPERUSER;"

# Проверяем существование базы данных
echo "Checking if database $DB_NAME exists..."
if PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U postgres -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Database $DB_NAME already exists"
else
    echo "Creating database $DB_NAME..."
    PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
    echo "Database $DB_NAME created successfully"
fi

# Даем все права на базу данных пользователю
echo "Granting all privileges on $DB_NAME to $DB_USER..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Database initialization completed"

# Запускаем основное приложение
exec python main.py 