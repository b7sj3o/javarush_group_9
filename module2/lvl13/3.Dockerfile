ARG BASE=python:3.12-slim
FROM ${BASE}
ARG REQ=requirements.txt
WORKDIR /app
COPY ${REQ} requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
COPY *.py .
CMD ["python", "bot.py"]
