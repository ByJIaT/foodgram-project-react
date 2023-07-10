FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN poetry install

COPY . .

