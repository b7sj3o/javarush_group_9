ARG VERSION=12

FROM python:3.${VERSION}-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "bot.py"]

