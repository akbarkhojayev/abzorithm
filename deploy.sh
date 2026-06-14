#!/bin/bash

# Deployment Script for algo.codialinfo.uz
# Usage: ./deploy.sh

set -e

echo "================================"
echo "Starting Deployment Process"
echo "================================"

# Variables
SERVER_IP="135.116.81.54"
SSH_KEY="$PWD/abzor.pem"
SERVER_USER="ubuntu"
PROJECT_DIR="/home/ubuntu/abzorithm"
DOMAIN="algo.codialinfo.uz"

echo ""
echo "Step 1: Checking SSH Key..."
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key not found: $SSH_KEY"
    exit 1
fi
chmod 600 "$SSH_KEY"
echo "✅ SSH key found and configured"

echo ""
echo "Step 2: Building Frontend..."
cd frontend
npm install
npm run build
cd ..
echo "✅ Frontend built successfully"

echo ""
echo "Step 3: Backing up old project on server..."
ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" \
    "cd /home/$SERVER_USER && \
    if [ -d abzortihm ]; then \
        sudo mv abzortihm abzortihm.backup.\$(date +%s); \
        echo 'Old project backed up'; \
    fi"
echo "✅ Old project backed up"

echo ""
echo "Step 4: Creating project directory..."
ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" \
    "sudo mkdir -p $PROJECT_DIR && \
    sudo chown $SERVER_USER:$SERVER_USER $PROJECT_DIR"
echo "✅ Project directory created"

echo ""
echo "Step 5: Uploading project files..."
scp -i "$SSH_KEY" -r frontend/dist "$SERVER_USER@$SERVER_IP:$PROJECT_DIR/"
scp -i "$SSH_KEY" -r frontend/public "$SERVER_USER@$SERVER_IP:$PROJECT_DIR/" 2>/dev/null || true
scp -i "$SSH_KEY" frontend-nginx.conf "$SERVER_USER@$SERVER_IP:/tmp/"
echo "✅ Files uploaded"

echo ""
echo "Step 6: Configuring Nginx..."
ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" \
    "sudo cp /tmp/frontend-nginx.conf /etc/nginx/sites-available/$DOMAIN && \
    sudo ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/$DOMAIN && \
    sudo rm -f /etc/nginx/sites-enabled/default && \
    sudo nginx -t && \
    sudo systemctl reload nginx"
echo "✅ Nginx configured"

echo ""
echo "Step 7: Setting up SSL Certificate..."
ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" \
    "sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m admin@$DOMAIN 2>/dev/null || echo 'SSL setup skipped'"
echo "✅ SSL configuration attempted"

echo ""
echo "================================"
echo "✅ Deployment Complete!"
echo "================================"
echo ""
echo "Website: https://$DOMAIN"
echo ""
echo "Next steps:"
echo "1. Update DNS records to point to $SERVER_IP"
echo "2. Wait 5-10 minutes for DNS propagation"
echo "3. Visit https://$DOMAIN"
echo ""
