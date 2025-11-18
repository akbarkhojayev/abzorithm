# 🐳 Abzorithm - Docker bilan 0 dan Ishga Tushirish

Bu qo'llanma sizga Abzorithm platformasini Docker yordamida 0 dan ishga tushirishda yordam beradi.

---

## 📋 Talablar

Sizning kompyuteringizda quyidagilar bo'lishi kerak:
- **Linux** operatsion tizimi (Ubuntu 20.04+ tavsiya etiladi)
- **Git** - kod yuklab olish uchun
- **Docker** va **Docker Compose** - konteynerlar uchun

---

## 🚀 Qadamma-Qadam O'rnatish

### 1️⃣ Docker O'rnatish

Agar Docker o'rnatilmagan bo'lsa:

```bash
# Docker o'rnatish scripti
chmod +x install_docker.sh
./install_docker.sh
```

Yoki qo'lda o'rnatish:

```bash
# Paketlarni yangilash
sudo apt-get update -y

# Kerakli paketlar
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Docker GPG kaliti
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker o'rnatish
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Foydalanuvchini docker guruhiga qo'shish
sudo usermod -aG docker $USER

# Docker servisni ishga tushirish
sudo systemctl enable docker
sudo systemctl start docker
```

**MUHIM:** Docker o'rnatgandan keyin terminaldan chiqib qayta kiring yoki quyidagi buyruqni bajaring:
```bash
newgrp docker
```

Docker tekshirish:
```bash
docker --version
docker compose version
```

---

### 2️⃣ Loyihani Yuklab Olish

```bash
# Repository'ni clone qiling
git clone https://github.com/yourusername/abzorithm.git
cd abzorithm
```

---

### 3️⃣ Docker Image'larni Yaratish

**Variant 1: Avtomatik (tavsiya etiladi)**

```bash
# Setup scriptga ruxsat berish
chmod +x docker_setup.sh

# Scriptni ishga tushirish
./docker_setup.sh
```

**Variant 2: Qo'lda**

```bash
# Code executor image yaratish
docker build -t abzorithm_code_executor -f Dockerfile.executor .

# Main application image yaratish
docker build -t abzorithm_main -f Dockerfile .

# Docker Compose bilan ishga tushirish
docker compose up -d
```

---

### 4️⃣ Database Sozlash

Container ichida database migratsiyalarini bajarish:

```bash
# Container ichiga kirish
docker compose exec abzorithm bash

# Migratsiyalar
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Container'dan chiqish
exit
```

Yoki bir qatorda:

```bash
# Migratsiyalar
docker compose exec abzorithm python manage.py migrate

# Superuser yaratish (interaktiv)
docker compose exec -it abzorithm python manage.py createsuperuser
```

---

### 5️⃣ Test Masalalarni Yuklash (ixtiyoriy)

```bash
# String masalalar
docker compose exec abzorithm python manage.py load_string_problems

# LeetCode masalalar
docker compose exec abzorithm python manage.py load_leetcode_problems

# Qo'shimcha matematik masalalar
docker compose exec abzorithm python manage.py load_more_string_math
```

---

### 6️⃣ Platformani Ochish

Brauzeringizda quyidagi manzillarni oching:

- **Frontend**: http://localhost:8001
- **API Documentation (Swagger)**: http://localhost:8001/swagger/
- **Admin Panel**: http://localhost:8001/admin/

**Eslatma:** Agar 8000 port band bo'lsa, Docker 8001 portda ishga tushadi.

---

## 🎯 Asosiy Buyruqlar

### Serverni Boshqarish

```bash
# Serverni ishga tushirish
docker compose up -d

# Serverni to'xtatish
docker compose down

# Loglarni ko'rish
docker compose logs -f

# Faqat bitta servis loglari
docker compose logs -f abzorithm

# Container statusini ko'rish
docker compose ps

# Container ichiga kirish
docker compose exec abzorithm bash
```

### Image'larni Qayta Qurish

```bash
# Barcha image'larni qayta qurish
docker compose up --build -d

# Faqat bitta image
docker compose build abzorithm
docker compose up -d
```

### Tozalash

```bash
# Container'larni to'xtatish va o'chirish
docker compose down

# Volume'lar bilan birga o'chirish
docker compose down -v

# Barcha Docker resurslarini tozalash
docker system prune -a
```

---

## 🧪 Test Qilish

### Docker Executor Test

```bash
# Test scriptni ishga tushirish
python3 test_docker.py
```

### Manual Test

```bash
# Python kodni test qilish
docker run --rm abzorithm_code_executor python3 -c "print('Hello Docker')"

# Container ichida test
docker compose exec abzorithm python manage.py test
```

---

## 📊 Monitoring va Debugging

### Resource Usage

```bash
# Container resource usage
docker stats

# Disk usage
docker system df
```

### Loglar

```bash
# Barcha loglar
docker compose logs

# Oxirgi 100 qator
docker compose logs --tail=100

# Real-time loglar
docker compose logs -f

# Vaqt bilan
docker compose logs --timestamps
```

### Container Ichini Ko'rish

```bash
# Bash shell
docker compose exec abzorithm bash

# Python shell
docker compose exec abzorithm python manage.py shell

# Database shell
docker compose exec abzorithm python manage.py dbshell
```

---

## 🔧 Troubleshooting

### Problem: Docker image topilmadi

**Yechim:**
```bash
docker build -t abzorithm_code_executor -f Dockerfile.executor .
docker build -t abzorithm_main -f Dockerfile .
```

### Problem: Port band

**Yechim:**
```bash
# 8000 portni ishlatayotgan processni topish
sudo lsof -i :8000

# Yoki boshqa portda ishga tushirish
# docker-compose.yml da portni o'zgartiring: "8080:8000"
```

### Problem: Permission denied

**Yechim:**
```bash
# Faylga ruxsat berish
chmod +x docker_setup.sh

# Docker guruhiga qo'shish
sudo usermod -aG docker $USER
newgrp docker
```

### Problem: Container ishlamayapti

**Yechim:**
```bash
# Container statusini tekshirish
docker compose ps

# Loglarni ko'rish
docker compose logs abzorithm

# Container'ni qayta ishga tushirish
docker compose restart abzorithm
```

### Problem: Database xatoligi

**Yechim:**
```bash
# Migratsiyalarni qayta bajarish
docker compose exec abzorithm python manage.py migrate

# Database'ni reset qilish (EHTIYOT!)
docker compose down -v
docker compose up -d
docker compose exec abzorithm python manage.py migrate
```

---

## 🔒 Xavfsizlik

Docker container'larda quyidagi xavfsizlik choralari qo'llanilgan:

- ✅ **Network isolation**: `--network=none`
- ✅ **Memory limit**: 100MB
- ✅ **CPU limit**: 1 core
- ✅ **Read-only filesystem**
- ✅ **Non-root user**: 1000:1000
- ✅ **No privileges**: Barcha capabilities o'chirilgan
- ✅ **Timeout**: 2 soniya

---

## 📈 Performance

### Optimizatsiya

```bash
# Image size kamaytirish
docker image prune

# Build cache tozalash
docker builder prune

# Ishlatilmayotgan volume'larni o'chirish
docker volume prune
```

### Resource Limits

`docker-compose.yml` da sozlash:

```yaml
services:
  abzorithm:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
```

---

## 🎓 Qo'shimcha Ma'lumot

### Docker Compose Arxitektura

```
┌─────────────────────────────────────┐
│     Docker Compose Network          │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │  abzorithm   │  │    code-    │ │
│  │  (Django)    │  │  executor   │ │
│  │  Port: 8000  │  │  (Isolated) │ │
│  └──────────────┘  └─────────────┘ │
│         │                           │
│         ▼                           │
│  ┌──────────────┐                  │
│  │   SQLite DB  │                  │
│  │   (Volume)   │                  │
│  └──────────────┘                  │
└─────────────────────────────────────┘
```

### Fayl Tuzilishi

```
abzorithm/
├── Dockerfile                 # Main app image
├── Dockerfile.executor       # Code executor image
├── docker-compose.yml        # Services orchestration
├── docker_setup.sh           # Setup automation
├── install_docker.sh         # Docker installation
├── run_code.py              # Python executor
├── run_code_js.py           # JavaScript executor
├── run_code_dart.py         # Dart executor
└── test_docker.py           # Test script
```

---

## 📞 Yordam

Agar muammo yuzaga kelsa:

1. **Loglarni tekshiring**: `docker compose logs -f`
2. **Container statusini ko'ring**: `docker compose ps`
3. **Resource usage**: `docker stats`
4. **GitHub Issues**: Muammoni yozing
5. **Documentation**: README.md va README_DOCKER.md

---

## ✅ Tekshirish Ro'yxati

Ishga tushirishdan oldin:

- [ ] Docker o'rnatilgan (`docker --version`)
- [ ] Docker Compose o'rnatilgan (`docker compose version`)
- [ ] Git o'rnatilgan (`git --version`)
- [ ] Repository clone qilingan
- [ ] Docker image'lar yaratilgan
- [ ] Container'lar ishga tushgan (`docker compose ps`)
- [ ] Database migratsiyalari bajarilgan
- [ ] Superuser yaratilgan
- [ ] Browser'da ochildi (http://localhost:8000)

---

## 🎉 Tayyor!

Endi platformangiz Docker'da ishlamoqda!

**Keyingi qadamlar:**
1. Admin panel orqali masalalar qo'shing
2. Frontend'da ro'yxatdan o'ting
3. Masalalarni yeching
4. Leaderboard'da o'zingizni ko'ring

**Omad! 🚀**

---

Made with ❤️ by Abzorithm Team
