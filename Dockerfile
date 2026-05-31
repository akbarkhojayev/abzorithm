# Python 3.11 base image
FROM python:3.11-slim

# Non-root user yaratish
RUN groupadd -r codeuser && useradd -r -g codeuser codeuser

# Working directory
WORKDIR /app

# Faqat kerakli paketlarni o'rnatish
RUN apt-get update && apt-get install -y \
    gcc \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# Dart SDK o'rnatish - direct binary
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    unzip \
    && curl -o /tmp/dart.zip https://storage.googleapis.com/dart-archive/channels/stable/release/3.2.0/sdk/dartsdk-linux-x64-release.zip \
    && unzip -q /tmp/dart.zip -d / \
    && rm /tmp/dart.zip \
    && ln -s /dart-sdk/bin/* /usr/local/bin/ \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code execution script
COPY run_code.py .

# Permissions o'rnatish
RUN chown -R codeuser:codeuser /app
RUN chmod +x run_code.py

# Non-root user ga o'tish
USER codeuser

# Default command
CMD ["python", "run_code.py"]
