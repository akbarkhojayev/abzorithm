# 👤 Profil Sahifasi Yangi Funksiyalar

## 📸 Avatar Upload (Profil Rasmi)

### Xususiyatlar:
- ✅ Rasm yuklash (JPG, PNG, GIF)
- ✅ Real-time preview
- ✅ Avtomatik o'lcham optimizatsiyasi
- ✅ Sidebar va profil sahifasida ko'rinadi

### Qanday Ishlaydi:
1. Profile Info tabiga o'ting
2. "Change Photo" tugmasini bosing
3. Rasmni tanlang (max 5MB)
4. Preview ko'rinadi
5. "Save Changes" tugmasini bosing

### Backend:
- `UserUpdateSerializer` - avatar maydonini qo'shildi
- `MEDIA_ROOT` va `MEDIA_URL` sozlandi
- Pillow kutubxonasi o'rnatildi

### Frontend:
- FormData bilan multipart/form-data yuboriladi
- Avatar preview state management
- CSS bilan chiroyli ko'rinish

---

## 📊 Recent Activity (Oxirgi Faollik)

### Xususiyatlar:
- ✅ Oxirgi 5 ta submission ko'rsatiladi
- ✅ Problem nomi va status
- ✅ Submission vaqti
- ✅ Execution time
- ✅ Status badge (Accepted/Wrong Answer)

### Qanday Ishlaydi:
1. Profile sahifasiga kiring
2. "Recent Activity" tabini tanlang
3. Oxirgi submissionlaringizni ko'ring

### Backend:
- `SubmissionListSerializer` - problem_title qo'shildi
- `/submissions/?user={userId}` endpoint

### Frontend:
- `getUserSubmissions()` API metodi
- Activity list komponenti
- Status-based styling

---

## 🎨 UI/UX Yaxshilanishlar

### Avatar Upload Section:
```css
- Circular preview (100px)
- Gradient background
- Hover effects
- Upload button styling
```

### Activity Items:
```css
- Card-based layout
- Icon indicators (✓/✗)
- Hover animations
- Status badges
- Meta information
```

### Responsive Design:
- Mobile-friendly layout
- Flexbox/Grid
- Adaptive spacing

---

## 📝 API Endpoints

### Update Profile with Avatar
```http
PATCH /users/me/update/
Authorization: Bearer {token}
Content-Type: multipart/form-data

FormData:
  - bio: string
  - country: string
  - avatar: file (optional)
```

### Get User Submissions
```http
GET /submissions/?user={userId}
Authorization: Bearer {token}

Response:
[
  {
    "id": 1,
    "problem": 1,
    "problem_title": "Two Sum",
    "status": "Accepted",
    "submitted_at": "2025-10-01T10:30:00Z",
    "execution_time": 45.5
  }
]
```

---

## 🔧 Texnik Detalllar

### Dependencies:
```txt
Pillow==10.0.0  # Image processing
```

### Settings (settings.py):
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### URLs (urls.py):
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Model (models.py):
```python
class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
```

---

## 📂 Fayl Strukturasi

```
abzorithm/
├── media/                    # User uploads
│   └── avatars/             # Profile pictures
│       ├── user1_avatar.jpg
│       └── user2_avatar.png
├── frontend-react/
│   └── src/
│       └── pages/
│           ├── ProfilePage.js    # Avatar upload logic
│           └── ProfilePage.css   # Avatar styling
└── main/
    ├── models.py            # User model with avatar
    └── serializers.py       # Avatar serializer
```

---

## 🚀 Ishga Tushirish

### 1. Pillow o'rnating:
```bash
pip install Pillow==10.0.0
```

### 2. Migration qiling:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Media papkasini yarating:
```bash
mkdir -p media/avatars
```

### 4. Server'ni ishga tushiring:
```bash
python manage.py runserver
```

---

## ✅ Test Qilish

### Avatar Upload:
1. Login qiling
2. Profile sahifasiga o'ting
3. "Change Photo" bosing
4. Rasm tanlang
5. "Save Changes" bosing
6. Sahifani refresh qiling
7. Avatar ko'rinishini tekshiring

### Recent Activity:
1. Biror problemni yechib ko'ring
2. Profile sahifasiga qayting
3. "Recent Activity" tabini oching
4. Submissioningiz ko'rinishini tekshiring

---

## 🐛 Troubleshooting

### Avatar yuklanmayapti:
- Pillow o'rnatilganini tekshiring
- MEDIA_ROOT to'g'ri sozlanganini tekshiring
- media/avatars papkasi mavjudligini tekshiring
- File permissions to'g'riligini tekshiring

### Submissions ko'rinmayapti:
- Backend ishlab turganini tekshiring
- User ID to'g'ri yuborilayotganini tekshiring
- Console'da error borligini tekshiring

---

## 📈 Kelajak Rejalar

- [ ] Avatar crop/resize frontend'da
- [ ] Multiple image formats support
- [ ] Avatar delete functionality
- [ ] Activity pagination
- [ ] Filter by status
- [ ] Export submissions
- [ ] Submission details modal

---

**Yangilangan:** 2025-10-01
**Versiya:** 1.1.0
