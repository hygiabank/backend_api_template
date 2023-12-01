# syntax=docker/dockerfile:1
FROM python:3.11-slim

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY app app

CMD [ "python", "-m", "app" ]
