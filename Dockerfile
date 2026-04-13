FROM python:3.12.7-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Railway healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8080 || exit 1

CMD ["python", "app.py"]
