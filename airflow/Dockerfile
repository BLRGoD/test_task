FROM apache/airflow:2.6.3

# Переключаемся на airflow пользователя для установки пакетов
USER airflow

# Устанавливаем clickhouse-driver
RUN pip install --no-cache-dir clickhouse-driver
