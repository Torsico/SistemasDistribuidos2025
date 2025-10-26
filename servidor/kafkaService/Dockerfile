FROM python:3.11-slim

WORKDIR /kafkaService

COPY ./kafkaService/ .

COPY .. .

COPY ../requirements.txt .

# Instalamos todas las dependencias, incluyendo protobuf
RUN pip install --no-cache-dir -r requirements.txt