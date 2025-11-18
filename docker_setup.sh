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

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup complete! Platform is running at http://localhost:8000"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Run migrations: docker compose exec abzorithm python manage.py migrate"
    echo "   2. Create superuser: docker compose exec -it abzorithm python manage.py createsuperuser"
    echo "   3. Load problems: docker compose exec abzorithm python manage.py load_string_problems"
    echo "   4. Open browser: http://localhost:8000"
    echo ""
    echo "🎯 Useful commands:"
    echo "   Stop: docker compose down"
    echo "   Logs: docker compose logs -f"
    echo "   Rebuild: docker compose up --build -d"
else
    echo "❌ Failed to start services"
    exit 1
fi
