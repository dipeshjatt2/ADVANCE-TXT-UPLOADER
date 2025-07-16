FROM python:3.10.8-buster

# Install system dependencies + Supervisor
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    musl-dev \
    ffmpeg \
    aria2 \
    supervisor \  # <-- Added for process management
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt pytube gunicorn

# Copy app files
COPY . .

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/

# Environment variables
ENV COOKIES_FILE_PATH="youtube_cookies.txt" \
    PORT=8000

# Start Supervisor
CMD ["supervisord", "-n"]
