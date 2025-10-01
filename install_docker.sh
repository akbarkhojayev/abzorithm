#!/bin/bash

# Docker o'rnatish script
echo "🐳 Docker o'rnatilmoqda..."

# Paketlar yangilash
sudo apt-get update -y

# Kerakli paketlarni o'rnatish
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Docker GPG kalitini qo'shish
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Docker repository qo'shish
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Paketlar yangilash
sudo apt-get update -y

# Docker o'rnatish
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Foydalanuvchini docker guruhiga qo'shish
sudo usermod -aG docker $USER

# Docker servisni yoqish
sudo systemctl enable docker
sudo systemctl start docker

echo "✅ Docker o'rnatildi!"
echo "⚠️  Foydalanuvchi docker guruhiga qo'shildi."
echo "👉 Iltimos, terminaldan chiqib qayta kiring yoki 'newgrp docker' buyrug'ini yozing."

# Test Docker (sudo ishlatmasdan)
echo "🧪 Docker test qilinmoqda..."
docker run hello-world

echo "🚀 Docker tayyor!"
