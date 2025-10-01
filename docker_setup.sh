#!/bin/bash

# Docker setup script for Abzorithm platform

echo "🐳 Docker setup for Abzorithm platform..."

# Docker image yaratish
echo "Building Docker images..."
docker build -t abzorithm_code_executor -f Dockerfile.executor .

if [ $? -eq 0 ]; then
    echo "✅ Code executor image built successfully"
else
    echo "❌ Failed to build code executor image"
    exit 1
fi

# Main application image
docker build -t abzorithm_main .

if [ $? -eq 0 ]; then
    echo "✅ Main application image built successfully"
else
    echo "❌ Failed to build main application image"
    exit 1
fi

echo "🚀 Starting services with docker compose..."
docker compose up -d

echo "✅ Setup complete! Platform is running at http://localhost:8000"
echo ""
echo "To stop the platform: docker compose down"
echo "To view logs: docker compose logs -f"
echo "To rebuild: docker compose up --build"
