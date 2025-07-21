FROM python:3.13.5-slim

WORKDIR /app

# Install curl (and remove cache from apt to keep the image size small)
RUN apt-get update \
 && apt-get install -y curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV NTFY_TOPIC=""
ENV NTFY_TOKEN=""
ENV HEARTBEAT_TIMEOUT=180
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]