# ⚡ Tez Start - Docker bilan

5 daqiqada ishga tushiring!

---

## 1️⃣ Docker O'rnatish

```bash
# Docker o'rnatish
chmod +x install_docker.sh
./install_docker.sh

# Terminal'dan chiqib qayta kiring yoki:
newgrp docker
```

---

## 2️⃣ Loyihani Ishga Tushirish

```bash
# Setup script
chmod +x docker_setup.sh
./docker_setup.sh
```

---

## 3️⃣ Database Sozlash

```bash
# Migratsiyalar
docker compose exec abzorithm python manage.py migrate

# Superuser yaratish
docker compose exec -it abzorithm python manage.py createsuperuser

# Test masalalar yuklash (ixtiyoriy)
docker compose exec abzorithm python manage.py load_string_problems
```

---

## 4️⃣ Ochish

Browser'da: **http://localhost:8001**

---

## 🎯 Asosiy Buyruqlar

```bash
# Ishga tushirish
docker compose up -d

# To'xtatish
docker compose down

# Loglar
docker compose logs -f

# Qayta ishga tushirish
docker compose restart
```

---

## 🔧 Muammo Bo'lsa

```bash
# Container statusini ko'rish
docker compose ps

# Loglarni tekshirish
docker compose logs abzorithm

# Qayta qurish
docker compose up --build -d
```

---

## ✅ Tayyor!

Platform ishlamoqda: http://localhost:8001

Admin panel: http://localhost:8001/admin/

API docs: http://localhost:8001/swagger/
