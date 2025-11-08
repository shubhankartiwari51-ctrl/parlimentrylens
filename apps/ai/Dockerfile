FROM python:3.11-slim

WORKDIR /app

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install build tools + Tesseract OCR
RUN apt-get update && apt-get install -y gcc g++ wget tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app
COPY app ./app

EXPOSE 8001
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
