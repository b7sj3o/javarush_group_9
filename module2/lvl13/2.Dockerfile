FROM python:3.12-slim
WORKDIR /app

COPY . .

RUN rm -f .env

CMD ["python", "bot.py"]
