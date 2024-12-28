FROM python:3.9-slim

RUN pip install dbt clickhouse-driver

WORKDIR /usr/app

COPY . /usr/app

ENTRYPOINT ["dbt"]
