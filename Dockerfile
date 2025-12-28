# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
# Install gcc and other tools often needed for building python libs
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# NOTE: In a real production environment, you might mount the vector DB volume.
# For this challenge package, we assume 'ingest.py' has been run locally 
# and the 'chroma_db' folder is copied into the container.
# Alternatively, you could uncomment the line below to run ingestion during build:
# RUN python ingest.py

# Expose port
EXPOSE 8000

# Run command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]