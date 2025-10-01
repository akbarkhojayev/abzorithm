# 🐳 Abzorithm Docker Setup

Bu platform Docker container yordamida xavfsiz kod ishga tushirish imkonini beradi.

## 🚀 Tez Start

```bash
# 1. Docker image yaratish
./docker_setup.sh

# 2. Yoki qo'lda:
docker-compose up -d

# 3. Test qilish
python3 test_docker.py
```
p
## 📁 Fayl Tuzilishi

```
├── Dockerfile                 # Asosiy application
├── Dockerfile.executor       # Kod ishga tushirish uchun
├── docker-compose.yml        # Services orchestration
├── run_code.py              # Xavfsiz kod runner
├── main/utils_docker.py     # Docker integration
├── test_docker.py           # Test script
└── docker_setup.sh          # Setup script
```

## 🔒 Xavfsizlik Xususiyatlari

### Container Isolation
- **Network yo'q**: `--network=none`
- **Memory cheklash**: 100MB RAM
- **CPU cheklash**: 1 CPU core
- **Read-only filesystem**: Fayl tizimiga yozish yo'q
- **Non-root user**: 1000:1000 user ID
- **No privileges**: Barcha capabilities o'chirilgan

### Resource Limits
- **CPU**: 2 soniya timeout
- **RAM**: 100MB maksimal
- **File size**: 5MB maksimal
- **Process count**: 20 ta maksimal

### Code Restrictions
- **Import cheklash**: os, subprocess, socket va boshqalar
- **Safe eval**: `ast.literal_eval()` ishlatiladi
- **Output cheklash**: 1000 character maksimal

## 🛠️ Manual Setup

### 1. Docker Images Yaratish

```bash
# Code executor image
docker build -t abzorithm_code_executor -f Dockerfile.executor .

# Main application image
docker build -t abzorithm_main .
```

### 2. Services Ishga Tushirish

```bash
# Docker Compose
docker-compose up -d

# Yoki individual
docker run -d -p 8000:8000 abzorithm_main
```

### 3. Test Qilish

```bash
# Test script
python3 test_docker.py

# Manual test
docker run --rm abzorithm_code_executor 'print("Hello")' 'input' 'output'
```

## 📊 Monitoring

```bash
# Loglarni ko'rish
docker-compose logs -f

# Container status
docker-compose ps

# Resource usage
docker stats
```

## 🔧 Troubleshooting

### Docker Image Topilmadi
```bash
docker build -t abzorithm_code_executor -f Dockerfile.executor .
```

### Permission Xatolik
```bash
sudo chown -R $USER:$USER .
chmod +x *.sh *.py
```

### Memory Cheklash
```bash
# Docker da memory oshirish
docker run --memory=200m abzorithm_code_executor
```

## 🚨 Xavfsizlik Eslatmalari

1. **Container avtomatik o'chadi** - `--rm` flag
2. **Tarmoq yo'q** - tashqi ulanishlar mumkin emas
3. **Read-only filesystem** - fayl yozish mumkin emas
4. **Non-root user** - kam huquqlar
5. **Resource limits** - CPU/RAM cheklash

## 📈 Performance

- **Startup time**: ~2-3 soniya
- **Memory usage**: ~50-100MB
- **Execution time**: <2 soniya
- **Cleanup**: Avtomatik

## 🔄 Updates

```bash
# Images yangilash
docker-compose down
docker-compose up --build -d

# Cleanup
docker system prune -a
```
