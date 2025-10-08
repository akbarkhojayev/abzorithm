# 🚀 Abzorithm - Coding Challenge Platform

**From Junior to Google Engineer**

Abzorithm - bu algoritmik masalalarni yechish va dasturlash ko'nikmalarini oshirish uchun mo'ljallangan zamonaviy platforma.

![Status](https://img.shields.io/badge/status-ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.2.6-green)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow)

---

## 📋 Mundarija

- [Xususiyatlar](#-xususiyatlar)
- [Texnologiyalar](#-texnologiyalar)
- [O'rnatish](#-ornatish)
- [Ishga Tushirish](#-ishga-tushirish)
- [Hujjatlar](#-hujjatlar)
- [Arxitektura](#-arxitektura)
- [API](#-api)
- [Hissa Qo'shish](#-hissa-qoshish)

---

## ✨ Xususiyatlar

### 🔐 Authentication
- User registration va login
- JWT token-based authentication
- Session persistence
- Secure password handling

### 📚 Problems
- Turli qiyinlik darajasidagi masalalar
- Tag-based filtering
- Detailed problem descriptions
- Input/Output examples

### 💻 Code Editor
- Syntax highlighting (Python)
- Auto-completion
- Theme toggle (Light/Dark)
- Font size control
- Code formatting
- Keyboard shortcuts

### ✅ Code Execution
- Real-time code validation
- Multiple test cases
- Detailed error messages
- Execution time tracking
- Automatic scoring

### 🏆 Leaderboard
- Global rankings
- Score-based sorting
- User statistics
- Country information

### 👤 Profile Management
- View user information
- Update profile details (bio, country)
- **Avatar upload** - Profile picture management
- Change password
- **Recent activity** - View last 5 submissions
- User statistics (score, solved problems)

---

## 🛠 Texnologiyalar

### Backend
- **Django 5.2.6** - Web framework
- **Django REST Framework** - API
- **SQLite** - Database
- **JWT** - Authentication
- **Docker** - Code execution (isolated environment)
- **Swagger/OpenAPI** - API documentation

### Frontend
- **Vanilla JavaScript (ES6+)** - No frameworks
- **CodeMirror** - Code editor
- **Font Awesome** - Icons
- **CSS3** - Styling
- **HTML5** - Markup

### DevOps
- **Git** - Version control
- **Python venv** - Virtual environment

---

## 📦 O'rnatish

### Talablar
- Python 3.12+
- pip
- Git
- Docker (optional, for code execution)

### 1. Repository'ni Clone qiling
```bash
git clone https://github.com/yourusername/abzorithm.git
cd abzorithm
```

### 2. Virtual Environment yarating
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# yoki
.venv\Scripts\activate  # Windows
```

### 3. Dependencies o'rnating
```bash
pip install -r requirements.txt
```

**Eslatma:** Pillow kutubxonasi profil rasmlari uchun kerak.

### 4. Database yarating
```bash
python manage.py migrate
```

### 5. Superuser yarating
```bash
python manage.py createsuperuser
```

### 6. Static files to'plang (optional)
```bash
python manage.py collectstatic
```

---

## 🚀 Ishga Tushirish

### Backend Server
```bash
cd /path/to/abzorithm
python manage.py runserver
```
Backend `http://localhost:8000` da ishga tushadi.

### Frontend Server
Yangi terminal oynasida:
```bash
cd /path/to/abzorithm/frontend
python -m http.server 8080
```
Frontend `http://localhost:8080` da ishga tushadi.

### Brauzerda Oching
```
http://localhost:8080
```

---

## 📚 Hujjatlar

### Asosiy Hujjatlar
- **[QUICK_START.md](QUICK_START.md)** - Tez boshlash qo'llanmasi
- **[FRONTEND_FIXES.md](FRONTEND_FIXES.md)** - Frontend texnik hujjat
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - O'zgarishlar hisoboti

### API Documentation
- Swagger UI: `http://localhost:8000/`
- Admin Panel: `http://localhost:8000/admin/`

---

## 🏗 Arxitektura

### Backend Structure
```
abzorithm/
├── core/                 # Django project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI config
├── main/                # Main application
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── utils.py         # Helper functions
│   └── utils_docker.py  # Code execution
├── frontend/            # Frontend files
│   ├── index.html       # Main HTML
│   ├── js/              # JavaScript files
│   └── styles/          # CSS files
├── manage.py            # Django management
└── requirements.txt     # Python dependencies
```

### Frontend Structure
```
frontend/
├── index.html           # Main page
├── js/
│   ├── api.js          # API integration
│   ├── auth.js         # Authentication
│   ├── main.js         # Main app logic
│   ├── problems.js     # Problems management
│   ├── problem-solver.js  # Code editor & submission
│   ├── leaderboard.js  # Leaderboard
│   ├── profile.js      # Profile management
│   └── code-editor.js  # CodeMirror setup
└── styles/
    └── main.css        # Styles
```

### Database Models
- **User** - Custom user model with score
- **Problem** - Coding problems
- **TestCase** - Test cases for problems
- **Submission** - User code submissions

---

## 🔌 API

### Authentication
```http
POST /token/
Content-Type: application/x-www-form-urlencoded

username=user&password=pass
```

### Get Current User
```http
GET /users/me/
Authorization: Bearer {token}
```

### Get Problems
```http
GET /problems/
```

### Submit Code
```http
POST /submissions/create/
Authorization: Bearer {token}
Content-Type: application/json

{
  "user": 1,
  "problem": 1,
  "code": "class Solution:\n    def solve(self):\n        pass",
  "language": "python"
}
```

### Response Format
```json
{
  "id": 123,
  "status": "Accepted",
  "execution_time": 45,
  "user_score": 11
}
```

Batafsil API hujjatlari: `http://localhost:8000/`

---

## 🤝 Hissa Qo'shish

### Development Setup
1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. Commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

### Code Style
- Python: PEP 8
- JavaScript: ES6+ standards
- Indentation: 4 spaces (Python), 2 spaces (JS)
- Comments: English yoki O'zbek

---

## 🐛 Bug Report

Agar bug topsangiz:
1. Issue oching GitHub'da
2. Bug'ni batafsil tasvirlab bering
3. Reproduction steps yozing
4. Screenshot qo'shing (agar kerak bo'lsa)

---

## 📝 License

This project is licensed under the MIT License.

---

## 👥 Authors

- **Akbar Khojayev** - Initial work

---

## 🙏 Acknowledgments

- LeetCode - Inspiration
- CodeForces - Problem ideas
- Django Community
- Open Source Community

---

## 📞 Contact

- GitHub: [@akbarkhojayev](https://github.com/akbarkhojayev)
- Email: contact@abzorithm.uz

---

## 📊 Status

### Current Version: 1.0.0

### Features Status
- ✅ Authentication System
- ✅ Problem Management
- ✅ Code Editor
- ✅ Code Execution
- ✅ Leaderboard
- ✅ Profile Management
- ⏳ Discussion Forum (Coming Soon)
- ⏳ Editorial Solutions (Coming Soon)
- ⏳ Contest Mode (Coming Soon)

### Browser Support
- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

---

## 🎯 Roadmap

### Version 1.1 (Planned)
- [ ] Submission history page
- [ ] User statistics dashboard
- [ ] Problem difficulty algorithm
- [ ] Code sharing feature

### Version 1.2 (Planned)
- [ ] Discussion forum
- [ ] Editorial solutions
- [ ] Multiple language support (Java, C++, JavaScript)
- [ ] Contest mode

### Version 2.0 (Future)
- [ ] Mobile app
- [ ] Real-time multiplayer
- [ ] AI-powered hints
- [ ] Video tutorials

---

## 💡 Tips

### For Users
- Start with Easy problems
- Read problem descriptions carefully
- Test your code with examples first
- Check execution time
- Learn from others on leaderboard

### For Developers
- Follow code style guidelines
- Write tests for new features
- Update documentation
- Check console for errors
- Use browser DevTools

---

## 🔒 Security

### Reporting Security Issues
If you discover a security vulnerability, please email security@abzorithm.uz

### Security Features
- JWT token authentication
- Password hashing (Django's default)
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS prevention
- Code execution in isolated Docker containers

---

## 📈 Performance

### Benchmarks
- Page load: < 2s
- API response: < 500ms
- Code execution: 1-5s (depends on code)
- Database queries: < 100ms

### Optimization
- Lazy loading
- Code splitting
- Database indexing
- Caching (planned)

---

**Happy Coding! 🚀**

Made with ❤️ by Abzorithm Team
