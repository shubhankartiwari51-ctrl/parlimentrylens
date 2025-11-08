# Use an official Python image
FROM python:3.11-slim

# Make logs unbuffered
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# Workdir
WORKDIR /code

# ---- Tesseract (with Hindi) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-hin \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python deps
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt

# App code
COPY . /code/

# Spaces expects 7860
EXPOSE 7860
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
