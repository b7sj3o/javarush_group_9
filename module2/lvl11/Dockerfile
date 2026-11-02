# Базовий образ: Linux + Python 3.12
FROM python:3.12-slim

# Робоча папка всередині контейнера
WORKDIR /app

# Спершу залежності, потім код (так кешуються шари)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Що виконати при запуску контейнера
CMD ["python", "main.py"]
