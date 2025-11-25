# 🚀 Abzorithm - Multi-Language Coding Platform

**From Junior to Google Engineer**

Abzorithm - bu Python, JavaScript va Dart tillarida algoritmik masalalarni yechish va dasturlash ko'nikmalarini oshirish uchun mo'ljallangan zamonaviy platforma.

![Status](https://img.shields.io/badge/status-production-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Django](https://img.shields.io/badge/django-5.2.6-green)
![Docker](https://img.shields.io/badge/docker-enabled-blue)
![Languages](https://img.shields.io/badge/languages-Python%20%7C%20JavaScript%20%7C%20Dart-orange)

---

## 📋 Mundarija

- [Xususiyatlar](#-xususiyatlar)
- [Texnologiyalar](#-texnologiyalar)
- [Tez Boshlash](#-tez-boshlash)
- [Docker bilan O'rnatish](#-docker-bilan-ornatish)
- [Manual O'rnatish](#-manual-ornatish)
- [Kod Bajarish Tizimi](#-kod-bajarish-tizimi)
- [API Hujjatlari](#-api-hujjatlari)
- [Arxitektura](#-arxitektura)
- [Xavfsizlik](#-xavfsizlik)

---

## ✨ Xususiyatlar

### 🌐 Multi-Language Support
- **Python** - Eng mashhur dasturlash tili
- **JavaScript (Node.js)** - Web development uchun
- **Dart** - Flutter va zamonaviy dasturlash

### 🔐 Authentication & Authorization
- JWT token-based authentication
- Secure password hashing
- Session management
- User registration va login

### 📚 Problem Management
- 3 xil qiyinlik darajasi (Easy, Medium, Hard)
- Tag-based filtering
- Slug-based URL routing
- Batafsil masala tavsiflari
- Input/Output examples

### 💻 Advanced Code Editor
- Multi-language syntax highlighting
- Auto-completion
- Theme toggle (Light/Dark)
- Font size control
- Code formatting
- Keyboard shortcuts
- Real-time validation

### ✅ Secure Code Execution
- **Docker-based isolation** - Har bir kod alohida containerda ishga tushadi
- **Resource limits** - CPU va memory cheklash
- **Network isolation** - Internet access yo'q
- **Security constraints** - Read-only filesystem, no privileges
- Multiple test cases
- Detailed error messages
- Execution time tracking

### 🏆 Leaderboard & Scoring
- Global rankings
- Score-based sorting (Easy: 5, Medium: 7, Hard: 10 points)
- User statistics
- Country information
- Real-time updates

### 👤 Profile Management
- Avatar upload
- Bio va country information
- Recent submissions (last 5)
- User statistics
- Password change

---

## 🛠 Texnologiyalar

### Backend
- **Django 5.2.6** - Web framework
- **Django REST Framework 3.15.2** - RESTful API
- **SQLite** - Development database
- **JWT (Simple JWT 5.3.0)** - Authentication
- **Docker** - Code execution isolation
- **drf-yasg** - Swagger/OpenAPI documentation
- **Pillow** - Image processing

### Code Execution
- **Python 3** - Python runtime
- **Node.js** - JavaScript runtime
- **Dart SDK 3.2.0** - Dart runtime
- **Docker** - Container isolation
- **subprocess** - Process management
- **tempfile** - Temporary file handling

### Frontend
- **Vanilla JavaScript (ES6+)** - No frameworks
- **CodeMirror** - Advanced code editor
- **Font Awesome** - Icons
- **CSS3** - Modern styling
- **Fetch API** - HTTP requests

### DevOps & Security
- **Docker Compose** - Multi-container orchestration
- **Security constraints** - no-new-privileges, cap_drop, read_only
- **Resource limits** - Memory: 200MB, CPU: 2 cores
- **Network isolation** - No internet access for code execution

---

## 🚀 Tez Boshlash

### Talablar
- **Docker** va **Docker Compose** (tavsiya etiladi)
- **Python 3.11+** (manual setup uchun)
- **Git**

### Docker bilan (Tavsiya etiladi)

```bash
# 1. Repository'ni clone qiling
git clone https://github.com/yourusername/abzorithm.git
cd abzorithm

# 2. Docker containerlarni build qiling
docker-compose build

# 3. Database migrate qiling
docker-compose run abzorithm python manage.py migrate

# 4. Superuser yarating
docker-compose run abzorithm python manage.py createsuperuser

# 5. Ishga tushiring
docker-compose up
```

Server `http://localhost:8001` da ishga tushadi.

### Qo'shimcha Hujjatlar
- **[DOCKER_SETUP_UZBEK.md](DOCKER_SETUP_UZBEK.md)** - Docker setup (O'zbek tilida)
- **[QUICK_DOCKER_START.md](QUICK_DOCKER_START.md)** - Tez Docker setup
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Batafsil setup qo'llanmasi

---

## 🐳 Docker bilan O'rnatish

### 1. Docker o'rnatish (agar yo'q bo'lsa)

```bash
# Ubuntu/Debian
./install_docker.sh

# Yoki manual
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. Project Setup

```bash
# Full setup (Docker + Database + Superuser)
./full_setup.sh

# Yoki qo'lda
docker-compose build
docker-compose run abzorithm python manage.py migrate
docker-compose run abzorithm python manage.py createsuperuser
```

### 3. Ishga Tushirish

```bash
# Background mode
docker-compose up -d

# Logs ko'rish
docker-compose logs -f

# To'xtatish
docker-compose down
```

### Docker Arxitektura

```yaml
services:
  abzorithm:           # Django web server
    - Port: 8001:8000
    - Volume: .:/app
    
  code-executor:       # Isolated code execution
    - Security: no-new-privileges, read-only
    - Network: none (isolated)
    - Resources: 200MB RAM, 2 CPU cores
```

---

## 💻 Manual O'rnatish

### 1. Virtual Environment

```bash
# Virtual environment yaratish
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Dependencies o'rnatish
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Migrate
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Static files (optional)
python manage.py collectstatic --noinput
```

### 3. Code Execution Scripts

Quyidagi fayllar kod bajarish uchun kerak:
- `run_code.py` - Python kod bajarish
- `run_code_js.py` - JavaScript kod bajarish
- `run_code_dart.py` - Dart kod bajarish

### 4. Ishga Tushirish

```bash
# Development server
python manage.py runserver

# Production (Gunicorn)
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

---

## 🔧 Kod Bajarish Tizimi

### Arxitektura

```
User Code → Django API → Docker Container → Language Runtime → Result
```

### Qo'llab-quvvatlanadigan Tillar

#### 1. Python
```python
class Solution:
    def solve(self, x):
        return x * 2
```

#### 2. JavaScript
```javascript
class Solution {
  solve(x) {
    return x * 2;
  }
}
```

#### 3. Dart
```dart
class Solution {
  dynamic solve(x) {
    return x * 2;
  }
}
```

### Xavfsizlik Choralari

1. **Docker Isolation** - Har bir kod alohida containerda
2. **Resource Limits**:
   - Memory: 200MB
   - CPU: 2 cores
   - Timeout: 2 seconds
3. **Network Isolation** - Internet yo'q
4. **Filesystem** - Read-only (faqat /tmp yozish mumkin)
5. **No Privileges** - Root access yo'q
6. **User Isolation** - Non-root user (codeuser)

### Kod Bajarish Jarayoni

```python
# 1. User kodni yuboradi
POST /submissions/create/
{
  "problem": 1,
  "code": "class Solution: ...",
  "language": "python"
}

# 2. Django API kod bajaradi
docker run --rm --memory=200m --cpus=2 \
  abzorithm_code_executor \
  python3 run_code.py "user_code" "input" "expected"

# 3. Natija qaytariladi
{
  "success": true,
  "status": "Accepted",
  "execution_time": 0.045,
  "message": "Test passed"
}
```

### Test Cases

Har bir masala uchun:
- **Public test cases** - Foydalanuvchi ko'radi
- **Hidden test cases** - Faqat submission vaqtida tekshiriladi
- **Order** - Test case tartibi

---

## 📡 API Hujjatlari

### Base URL
```
http://localhost:8001/api/
```

### Authentication

#### Register
```http
POST /users/create/
Content-Type: application/json

{
  "username": "john",
  "email": "john@example.com",
  "password": "securepass123"
}
```

#### Login
```http
POST /token/
Content-Type: application/x-www-form-urlencoded

username=john&password=securepass123
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Problems

#### List Problems
```http
GET /problems/
GET /problems/?difficulty=Easy
GET /problems/?tags=array
GET /problems/?search=two+sum
```

#### Get Problem Detail
```http
GET /problems/{slug}/
Authorization: Bearer {access_token}
```

### Submissions

#### Create Submission
```http
POST /submissions/create/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "problem": 1,
  "code": "class Solution:\n    def solve(self, x):\n        return x",
  "language": "python"
}
```

Response (Success):
```json
{
  "id": 123,
  "status": "Accepted",
  "execution_time": 0.045,
  "failed_test": null,
  "error_input": null,
  "error_expected": null,
  "error_output": null,
  "user_score": 15
}
```

Response (Failed):
```json
{
  "id": 124,
  "status": "Wrong Answer",
  "execution_time": 0.032,
  "failed_test": 2,
  "error_input": "5",
  "error_expected": "10",
  "error_output": "5",
  "user_score": 15
}
```

#### List Submissions
```http
GET /submissions/
GET /submissions/?user=1
Authorization: Bearer {access_token}
```

### User Profile

#### Get Current User
```http
GET /users/me/
Authorization: Bearer {access_token}
```

#### Update Profile
```http
PATCH /users/update/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

bio=Software Engineer
country=Uzbekistan
avatar=@profile.jpg
```

### Leaderboard
```http
GET /leaderboard/
```

### Swagger Documentation
```
http://localhost:8001/
```

---

## 🏗 Arxitektura

### Project Structure

```
abzorithm/
├── core/                      # Django project settings
│   ├── settings.py           # Configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI config
│
├── main/                      # Main application
│   ├── models.py             # Database models
│   │   ├── User              # Custom user with score
│   │   ├── Problem           # Coding problems
│   │   ├── TestCase          # Test cases
│   │   └── Submission        # User submissions
│   │
│   ├── views.py              # API views
│   │   ├── UserCreateView
│   │   ├── ProblemList/Detail
│   │   ├── SubmissionCreate
│   │   └── LeaderboardView
│   │
│   ├── serializers.py        # DRF serializers
│   ├── utils.py              # Helper functions
│   ├── utils_docker.py       # Docker code execution
│   └── filters.py            # Django filters
│
├── run_code.py               # Python executor
├── run_code_js.py            # JavaScript executor
├── run_code_dart.py          # Dart executor
│
├── Dockerfile                # Main app container
├── Dockerfile.executor       # Code execution container
├── docker-compose.yml        # Multi-container setup
│
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management
└── db.sqlite3               # SQLite database
```

### Database Schema

```sql
-- User Model
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(150) UNIQUE,
    email VARCHAR(254),
    password VARCHAR(128),
    bio TEXT,
    avatar VARCHAR(100),
    score INTEGER DEFAULT 0,
    country VARCHAR(100)
);

-- Problem Model
CREATE TABLE problem (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) UNIQUE,
    slug VARCHAR(100) UNIQUE,
    description TEXT,
    difficulty VARCHAR(10),  -- Easy, Medium, Hard
    input_example TEXT,
    output_example TEXT,
    tags VARCHAR(255),
    function_name VARCHAR(50),
    created_at DATETIME
);

-- TestCase Model
CREATE TABLE testcase (
    id INTEGER PRIMARY KEY,
    problem_id INTEGER REFERENCES problem(id),
    input_data TEXT,
    expected_output TEXT,
    order INTEGER,
    is_hidden BOOLEAN
);

-- Submission Model
CREATE TABLE submission (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES user(id),
    problem_id INTEGER REFERENCES problem(id),
    code TEXT,
    language VARCHAR(10),  -- python, javascript, dart
    status VARCHAR(20),    -- Accepted, Wrong Answer, etc.
    submitted_at DATETIME,
    execution_time FLOAT,
    failed_test INTEGER,
    error_input TEXT,
    error_expected TEXT,
    error_output TEXT
);
```

### Code Execution Flow

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ POST /submissions/create/
       ▼
┌─────────────────┐
│  Django API     │
│  (views.py)     │
└──────┬──────────┘
       │ run_python_function_docker()
       ▼
┌─────────────────┐
│ utils_docker.py │
│ Docker Runner   │
└──────┬──────────┘
       │ docker run abzorithm_code_executor
       ▼
┌──────────────────────────┐
│  Docker Container        │
│  ┌────────────────────┐  │
│  │ run_code_*.py      │  │
│  │ - Parse input      │  │
│  │ - Execute code     │  │
│  │ - Compare output   │  │
│  └────────────────────┘  │
│                          │
│  Runtimes:               │
│  - Python 3              │
│  - Node.js               │
│  - Dart SDK              │
└──────────┬───────────────┘
           │ JSON result
           ▼
    ┌─────────────┐
    │   Response  │
    │   to User   │
    └─────────────┘
```

---

## 🔒 Xavfsizlik

### Authentication
- **JWT Tokens** - Stateless authentication
- **Password Hashing** - Django's PBKDF2
- **Token Expiry** - Access: 60 min, Refresh: 1 day

### Code Execution Security

#### Docker Isolation
```yaml
security_opt:
  - no-new-privileges:true  # Privilege escalation yo'q
cap_drop:
  - ALL                     # Barcha capabilities olib tashlash
read_only: true             # Read-only filesystem
network_mode: "none"        # Internet yo'q
user: "1000:1000"          # Non-root user
```

#### Resource Limits
```python
--memory=200m    # 200MB RAM
--cpus=2         # 2 CPU cores
timeout=2        # 2 seconds timeout
```

#### Filesystem
```yaml
tmpfs:
  - /tmp:noexec,nosuid,size=100m  # Faqat /tmp yozish mumkin
```

### API Security
- **CORS** - Configured origins
- **CSRF Protection** - Django middleware
- **SQL Injection** - Django ORM protection
- **XSS Prevention** - Input sanitization

### Best Practices
1. Hech qachon production'da `DEBUG=True` ishlatmang
2. `SECRET_KEY` ni environment variable sifatida saqlang
3. HTTPS ishlatish (production)
4. Regular security updates
5. Database backups

---

## 📊 Performance

### Benchmarks
- **API Response**: < 100ms
- **Code Execution**: 0.5-2s (depends on code)
- **Database Queries**: < 50ms
- **Page Load**: < 1s

### Optimization
- Database indexing (slug, user_id, problem_id)
- Docker image caching
- Static file serving
- Query optimization (select_related, prefetch_related)

### Scalability
- Horizontal scaling (multiple containers)
- Load balancing (Nginx)
- Database migration (PostgreSQL)
- Caching (Redis)
- CDN for static files

Batafsil: [SCALABILITY_ANALYSIS.md](SCALABILITY_ANALYSIS.md)

---

## 🧪 Testing

### Manual Testing
```bash
# Test Python execution
python run_code.py "class Solution:\n    def solve(self, x):\n        return x" "5" "5"

# Test JavaScript execution
python run_code_js.py "class Solution { solve(x) { return x; } }" "5" "5"

# Test Dart execution
python run_code_dart.py "class Solution { dynamic solve(x) { return x; } }" "5" "5"
```

### Docker Testing
```bash
# Test Docker executor
python test_docker.py

# Test specific language
docker run --rm abzorithm_code_executor python3 run_code.py "..." "5" "5"
```

---

## 🐛 Troubleshooting

### Docker Issues

**Problem**: Docker build fails with "no space left"
```bash
# Solution: Clean Docker
docker system prune -a --volumes -f
sudo apt-get clean
sudo journalctl --vacuum-size=50M
```

**Problem**: Dart not found in container
```bash
# Solution: Rebuild executor image
docker build -t abzorithm_code_executor -f Dockerfile.executor . --no-cache
```

### Code Execution Issues

**Problem**: "RuntimeError: [Errno 2] No such file or directory: 'dart'"
```bash
# Solution: Check Dart installation in container
docker run --rm abzorithm_code_executor dart --version
```

**Problem**: "Too many positional arguments"
```bash
# Solution: Use Function.apply() for dynamic arguments (already implemented)
```

### Database Issues

**Problem**: Migration errors
```bash
# Solution: Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🤝 Contributing

### Development Setup
1. Fork repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

### Code Style
- **Python**: PEP 8, Black formatter
- **JavaScript**: ES6+, Prettier
- **Indentation**: 4 spaces (Python), 2 spaces (JS)
- **Comments**: English

### Adding New Language

1. Create executor script: `run_code_<language>.py`
2. Update `Dockerfile.executor` with runtime
3. Add to `utils_docker.py` executor_map
4. Update `Submission.LANGUAGE_CHOICES`
5. Add frontend support
6. Write tests

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Akbar Khojayev** - Initial work & Development

---

## 🙏 Acknowledgments

- **LeetCode** - Platform inspiration
- **CodeForces** - Problem ideas
- **Django Community** - Framework support
- **Docker** - Containerization
- **Open Source Community** - Tools and libraries

---

## 📞 Contact

- **GitHub**: [@akbarkhojayev](https://github.com/akbarkhojayev)
- **Email**: contact@abzorithm.uz
- **Website**: https://abzorithm.uz

---

## 🎯 Roadmap

### Version 1.1 (Current)
- ✅ Multi-language support (Python, JavaScript, Dart)
- ✅ Docker-based code execution
- ✅ Security hardening
- ✅ Profile management

### Version 1.2 (Planned)
- [ ] More languages (Java, C++, Go, Rust)
- [ ] Discussion forum
- [ ] Editorial solutions
- [ ] Contest mode
- [ ] Code sharing

### Version 2.0 (Future)
- [ ] Real-time multiplayer
- [ ] AI-powered hints
- [ ] Video tutorials
- [ ] Mobile app
- [ ] Company-specific problems

---

## 💡 Tips

### For Users
- Start with **Easy** problems
- Read problem descriptions carefully
- Test with examples first
- Check execution time
- Learn from leaderboard

### For Developers
- Use Docker for consistent environment
- Follow security best practices
- Write tests for new features
- Update documentation
- Monitor resource usage

---

**Happy Coding! 🚀**

Made with ❤️ in Uzbekistan
