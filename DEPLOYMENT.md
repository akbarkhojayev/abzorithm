# Deployment Instructions - algo.codialinfo.uz

## Server Details
- **IP Address:** 135.116.81.54
- **Domain:** algo.codialinfo.uz
- **SSH Key:** abzor.pem
- **Server User:** ubuntu

## Quick Deployment (Recommended)

### Option 1: Automatic Deployment Script

```bash
cd /home/abz/Desktop/abzorithm
./deploy.sh
```

This script will:
1. ✅ Check SSH key
2. ✅ Build frontend
3. ✅ Backup old project
4. ✅ Upload new files
5. ✅ Configure Nginx
6. ✅ Setup SSL certificate

### Option 2: Manual Deployment

#### Step 1: Connect to Server
```bash
ssh -i abzor.pem ubuntu@135.116.81.54
```

#### Step 2: Backup Old Project
```bash
cd /home/ubuntu
sudo mv abzortihm abzortihm.backup.$(date +%s)
mkdir -p /home/ubuntu/abzorithm
cd /home/ubuntu/abzorithm
```

#### Step 3: Upload Files (From Local Machine)
```bash
cd /home/abz/Desktop/abzorithm
scp -i abzor.pem -r frontend/dist/* ubuntu@135.116.81.54:/home/ubuntu/abzorithm/
scp -i abzor.pem frontend-nginx.conf ubuntu@135.116.81.54:/tmp/
```

#### Step 4: Setup Nginx (On Server)
```bash
cd /home/ubuntu/abzorithm
sudo cp /tmp/frontend-nginx.conf /etc/nginx/sites-available/algo.codialinfo.uz
sudo ln -sf /etc/nginx/sites-available/algo.codialinfo.uz /etc/nginx/sites-enabled/algo.codialinfo.uz
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

#### Step 5: Setup SSL (Let's Encrypt)
```bash
sudo certbot --nginx -d algo.codialinfo.uz
```

## Post-Deployment

### 1. Update DNS Records
Point your domain's A record to:
```
algo.codialinfo.uz  A  135.116.81.54
```

### 2. Verify Deployment
```bash
curl https://algo.codialinfo.uz
```

### 3. Check Logs
```bash
# Nginx access logs
sudo tail -f /var/log/nginx/algo.codialinfo.uz.access.log

# Nginx error logs
sudo tail -f /var/log/nginx/algo.codialinfo.uz.error.log
```

### 4. SSL Renewal (Auto)
Certbot automatically renews SSL certificates. Verify:
```bash
sudo certbot renew --dry-run
```

## Troubleshooting

### Issue: Connection refused
```bash
# Check if Nginx is running
sudo systemctl status nginx

# Restart Nginx
sudo systemctl restart nginx
```

### Issue: 502 Bad Gateway
```bash
# Check API backend
curl http://localhost:8000/api/

# Restart backend (if applicable)
sudo systemctl restart your-backend-service
```

### Issue: SSL Certificate Error
```bash
# Renew certificate
sudo certbot renew

# Check certificate
sudo certbot certificates
```

## Rollback to Previous Version
```bash
sudo rm -rf /home/ubuntu/abzorithm
sudo mv /home/ubuntu/abzortihm.backup.* /home/ubuntu/abzortihm
sudo systemctl reload nginx
```

## Server Maintenance

### Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### Monitor Disk Space
```bash
df -h
```

### Check Server Resources
```bash
top
```

## Important Files

- **Frontend Build:** `/home/ubuntu/abzorithm/dist/`
- **Nginx Config:** `/etc/nginx/sites-available/algo.codialinfo.uz`
- **SSL Certs:** `/etc/letsencrypt/live/algo.codialinfo.uz/`
- **Nginx Logs:** `/var/log/nginx/algo.codialinfo.uz.*`

## Support

For deployment issues:
1. Check error logs
2. Verify SSH connectivity
3. Ensure DNS is pointing to correct IP
4. Contact server administrator

---

**Last Updated:** 2026-06-15
**Deployment Method:** Nginx + Let's Encrypt SSL
**Frontend Framework:** React (SPA)
