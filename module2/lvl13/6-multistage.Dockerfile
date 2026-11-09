# Етап 1: компілюємо там, де є gcc і заголовки libpq
FROM python:3.12 AS builder
WORKDIR /build
COPY requirements-pg.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements-pg.txt

# Етап 2: фінальний образ. Від builder беремо лише результат
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /install /usr/local
COPY *.py .
CMD ["python", "bot.py"]
