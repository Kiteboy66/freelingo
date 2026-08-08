FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV HF_HOME=/models/huggingface
EXPOSE 9100

CMD ["sh", "-c", "exec uvicorn app:app --host '' --port ${PORT:-9100}"]
