# Use an official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# --- This is the FIX ---
# Install Tesseract (with Hindi) and FFmpeg (for audio)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-hin \
    ffmpeg \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app ./app

# --- This is the FIX for the port ---
# Use the "shell" form to read the $PORT variable
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT