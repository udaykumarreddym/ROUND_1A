# Base image with Python (do not hardcode platform here)
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all local files into container
COPY . .

# Install system libraries required for PyMuPDF rendering
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure input/output folders exist in container
RUN mkdir -p /app/input /app/output

# Set default command to run your main.py
CMD ["python", "src/main.py"]
