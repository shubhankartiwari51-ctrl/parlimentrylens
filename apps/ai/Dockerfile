# Use an official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# --- This is the fix for Tesseract ---
# Install the Tesseract "scan engine" and the Hindi language pack
# Add 'tesseract-ocr-mar' for Marathi, etc.
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-hin \
    --no-install-recommends

# Copy and install Python requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all your app code into the container
COPY . /code/

# Tell the container what command to run on startup
# We use 0.0.0.0 (all IPs) and Render's $PORT variable
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]