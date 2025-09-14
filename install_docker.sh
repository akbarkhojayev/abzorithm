#!/bin/bash

# Docker o'rnatish script

echo "🐳 Docker o'rnatilmoqda..."

# Update package list
sudo apt-get update

# Install required packages
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again
sudo apt-get update

# Install Docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

echo "✅ Docker o'rnatildi!"
echo "⚠️  Logout va login qiling docker group uchun"
echo "Yoki: newgrp docker"

# Test Docker
echo "🧪 Docker test qilinmoqda..."
sudo docker run hello-world

echo "🚀 Docker tayyor! Endi ./docker_setup.sh ishga tushiring"
