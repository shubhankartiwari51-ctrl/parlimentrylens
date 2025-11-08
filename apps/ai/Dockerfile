# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /code

# ✅ Install Tesseract and Hindi pack (add others if needed)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-hin \
    --no-install-recommends

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy app code
COPY . /code/

# ✅ Start the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
