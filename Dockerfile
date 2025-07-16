FROM python:3.10.8-slim-buster

# Install system dependencies in separate RUN commands for better error handling
RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    musl-dev \
    ffmpeg \
    aria2 \
    supervisor

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt pytube gunicorn

# Copy app files
COPY . .

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Environment variables
ENV COOKIES_FILE_PATH="youtube_cookies.txt" \
    PORT=8000

# Start Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf", "-n"]
