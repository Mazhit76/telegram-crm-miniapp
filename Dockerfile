FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bot/ ./bot/
COPY miniapp/ ./miniapp/

WORKDIR /app/bot

CMD ["python", "main.py"]