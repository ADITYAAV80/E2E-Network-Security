FROM python:3.12-slim

WORKDIR /app

COPY . /app


RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt && docker cp .env my-container:/app/.env

CMD ["python3","main.py"]