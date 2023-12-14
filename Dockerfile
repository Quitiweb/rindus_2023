FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y build-essential

WORKDIR /app
COPY synchro_api /app
COPY requirements.txt /app
COPY manage.py /app
COPY .env /app

RUN pip install -r requirements.txt
