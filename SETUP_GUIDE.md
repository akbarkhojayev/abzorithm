# 🚀 Tez O'rnatish va Ishga Tushirish

## 📋 Qisqa Qo'llanma

### 1️⃣ Pillow O'rnatish
```bash
cd /home/abz/Desktop/abzorithm./abzorithm
pip install Pillow==10.0.0
```

### 2️⃣ Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3️⃣ Media Papka Yaratish
```bash
mkdir -p media/avatars
```

### 4️⃣ Backend Ishga Tushirish
```bash
python manage.py runserver
```

### 5️⃣ Frontend Ishga Tushirish
Yangi terminal oynasida:
```bash
cd frontend-react
npm start
```

---

## ✅ Yangi Funksiyalarni Test Qilish

### Avatar Upload:
1. `http://localhost:3000` ga kiring
2. Login qiling
3. Profile sahifasiga o'ting
4. "Profile Info" tabida "Change Photo" tugmasini bosing
5. Rasm tanlang va "Save Changes" bosing

### Recent Activity:
1. Profile sahifasida "Recent Activity" tabini oching
2. Oxirgi submissionlaringizni ko'ring
3. Agar submission yo'q bo'lsa, "Start Solving Problems" tugmasini bosing

---

## 🔍 Tekshirish

### Backend:
- ✅ `http://localhost:8000/admin` - Admin panel
- ✅ `http://localhost:8000/` - Swagger API docs
- ✅ `http://localhost:8000/users/me/` - Current user

### Frontend:
- ✅ `http://localhost:3000` - Main app
- ✅ `http://localhost:3000/profile` - Profile page

---

## 📝 Eslatmalar

1. **Pillow** - Rasm yuklash uchun zarur
2. **Media papka** - User rasmlari saqlanadi
3. **Migration** - Database yangilanadi
4. **CORS** - Frontend va Backend bir-biriga ulangan

---

## 🐛 Muammolar

### Pillow o'rnatilmasa:
```bash
pip install --upgrade pip
pip install Pillow==10.0.0
```

### Media papka yaratilmasa:
```bash
sudo mkdir -p media/avatars
sudo chmod 755 media
```

### Port band bo'lsa:
```bash
# Backend
python manage.py runserver 8001

# Frontend
PORT=3001 npm start
```

---

**Tayyor! Platformadan foydalaning! 🎉**
