FROM python:3.13.5-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV NTFY_TOPIC=""
ENV NTFY_TOKEN=""
ENV HEARTBEAT_TIMEOUT=180
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]