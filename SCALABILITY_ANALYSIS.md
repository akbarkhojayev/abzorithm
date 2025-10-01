# Scalability Analysis - Loyiha Sig'imi Tahlili

## 📊 Hozirgi Arxitektura

### Backend Stack
- **Framework:** Django 5.2.6 + Django REST Framework
- **Database:** SQLite (file-based)
- **Server:** Django development server (single-threaded)
- **Code Execution:** Docker containers
- **Authentication:** JWT (stateless)

### Frontend Stack
- **Type:** Static files (HTML, CSS, JS)
- **API Calls:** Fetch API (async)
- **State:** LocalStorage (client-side)

---

## 🎯 Concurrent Users Estimation

### Current Configuration (Development)

#### 1. Django Development Server
```python
# Single-threaded, synchronous
python manage.py runserver
```

**Capacity:** **1-5 concurrent users**
- ❌ Single thread
- ❌ No load balancing
- ❌ Blocks on I/O operations
- ❌ Not production-ready

#### 2. SQLite Database
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Capacity:** **10-20 concurrent users**
- ❌ File-based locking
- ❌ Single writer at a time
- ❌ Read-heavy workload OK
- ❌ Write-heavy workload bottleneck

#### 3. Code Execution (Docker)
```python
def run_python_function_docker(...):
    subprocess.run([
        'docker', 'run', 
        '--rm',
        '--memory=200m',
        '--cpus=2',
        ...
    ])
```

**Capacity:** **Depends on host resources**
- Each submission = 1 Docker container
- Memory per container: 200MB
- CPU per container: 2 cores
- Timeout: 2 seconds

**Calculation:**
- 8GB RAM → ~30 containers simultaneously
- 8 CPU cores → ~4 containers simultaneously
- **Bottleneck: CPU → 4 concurrent submissions**

---

## 📈 Realistic Capacity

### Scenario 1: Current Setup (Development)
```
Server: Django dev server (1 thread)
Database: SQLite
Host: 8GB RAM, 8 CPU cores
```

**Maximum Concurrent Users:** **3-5 users**

**Breakdown:**
- Browsing problems: 10-20 users ✅
- Viewing leaderboard: 10-20 users ✅
- Submitting code: **3-5 users** ❌ (bottleneck)

**Why?**
1. Django dev server blocks on each request
2. Docker container creation takes ~500ms
3. Code execution takes 1-3 seconds
4. Only 1 request processed at a time

---

### Scenario 2: Production Setup (Gunicorn)
```
Server: Gunicorn (4 workers)
Database: SQLite
Host: 8GB RAM, 8 CPU cores
```

**Maximum Concurrent Users:** **20-30 users**

**Breakdown:**
- Browsing problems: 50-100 users ✅
- Viewing leaderboard: 50-100 users ✅
- Submitting code: **20-30 users** ⚠️

**Configuration:**
```bash
gunicorn core.wsgi:application \
    --workers 4 \
    --threads 2 \
    --timeout 30 \
    --bind 0.0.0.0:8000
```

---

### Scenario 3: Production + PostgreSQL
```
Server: Gunicorn (8 workers)
Database: PostgreSQL
Host: 16GB RAM, 16 CPU cores
```

**Maximum Concurrent Users:** **100-200 users**

**Breakdown:**
- Browsing problems: 500-1000 users ✅
- Viewing leaderboard: 500-1000 users ✅
- Submitting code: **100-200 users** ✅

**Why Better?**
1. PostgreSQL handles concurrent writes
2. More workers = more parallel requests
3. Better resource utilization
4. Connection pooling

---

### Scenario 4: Production + Queue System
```
Server: Gunicorn (8 workers)
Database: PostgreSQL
Queue: Celery + Redis
Host: 32GB RAM, 32 CPU cores
```

**Maximum Concurrent Users:** **1000+ users**

**Breakdown:**
- Browsing problems: 5000+ users ✅
- Viewing leaderboard: 5000+ users ✅
- Submitting code: **1000+ users** ✅

**Architecture:**
```
User → Django → Celery Queue → Worker Pool → Docker
                    ↓
                PostgreSQL
```

---

## 🔍 Bottleneck Analysis

### 1. Django Development Server ⚠️⚠️⚠️
**Impact:** CRITICAL
- Single-threaded
- Blocks on each request
- **Solution:** Use Gunicorn/uWSGI

### 2. SQLite Database ⚠️⚠️
**Impact:** HIGH
- File locking
- Single writer
- **Solution:** Use PostgreSQL/MySQL

### 3. Synchronous Code Execution ⚠️⚠️
**Impact:** HIGH
- Blocks worker during execution
- No parallelization
- **Solution:** Use Celery + Redis

### 4. Docker Container Overhead ⚠️
**Impact:** MEDIUM
- 500ms startup time
- Resource limits
- **Solution:** Container pooling, Kubernetes

### 5. No Caching ⚠️
**Impact:** MEDIUM
- Repeated database queries
- No static file caching
- **Solution:** Redis cache, CDN

---

## 💡 Optimization Recommendations

### Phase 1: Quick Wins (1-2 days)
```bash
# 1. Use Gunicorn
pip install gunicorn
gunicorn core.wsgi:application --workers 4 --threads 2

# 2. Add database indexes
python manage.py makemigrations
python manage.py migrate

# 3. Enable gzip compression
# Add middleware in settings.py
```

**Result:** 5 → 30 concurrent users

---

### Phase 2: Database Migration (1 week)
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'abzorithm',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Result:** 30 → 100 concurrent users

---

### Phase 3: Async Queue (2 weeks)
```python
# Install Celery
pip install celery redis

# tasks.py
from celery import shared_task

@shared_task
def execute_code(submission_id):
    submission = Submission.objects.get(id=submission_id)
    # Execute code asynchronously
    ...

# views.py
def create(self, request):
    submission = serializer.save()
    execute_code.delay(submission.id)  # Async
    return Response({"id": submission.id, "status": "Pending"})
```

**Result:** 100 → 1000+ concurrent users

---

### Phase 4: Horizontal Scaling (1 month)
```yaml
# docker-compose.yml
services:
  web:
    image: abzorithm-web
    replicas: 4
  
  worker:
    image: abzorithm-worker
    replicas: 8
  
  db:
    image: postgres:15
  
  redis:
    image: redis:7
  
  nginx:
    image: nginx
    ports:
      - "80:80"
```

**Result:** 1000+ → 10,000+ concurrent users

---

## 📊 Cost Estimation

### Current Setup (Development)
- **Server:** Local machine (free)
- **Users:** 3-5 concurrent
- **Cost:** $0/month

### Small Production (VPS)
- **Server:** DigitalOcean Droplet (4GB RAM, 2 CPU)
- **Users:** 20-30 concurrent
- **Cost:** $24/month

### Medium Production (VPS + Database)
- **Server:** DigitalOcean Droplet (8GB RAM, 4 CPU)
- **Database:** Managed PostgreSQL
- **Users:** 100-200 concurrent
- **Cost:** $80/month

### Large Production (Kubernetes)
- **Cluster:** 3 nodes (16GB RAM, 8 CPU each)
- **Database:** Managed PostgreSQL (HA)
- **Redis:** Managed Redis
- **CDN:** Cloudflare
- **Users:** 1000+ concurrent
- **Cost:** $500-1000/month

---

## 🎯 Realistic Answer

### Current State (Development)
**Answer:** **3-5 concurrent users** (code submission)

**Limitations:**
- Django dev server (single-threaded)
- SQLite (file locking)
- Synchronous code execution
- No optimization

### With Minimal Changes (Gunicorn + PostgreSQL)
**Answer:** **50-100 concurrent users**

**Changes Needed:**
- Use Gunicorn (1 hour)
- Migrate to PostgreSQL (4 hours)
- Add basic caching (2 hours)
- Total: 1 day work

### With Full Optimization (Celery + Queue)
**Answer:** **500-1000+ concurrent users**

**Changes Needed:**
- Implement Celery (1 week)
- Add Redis (1 day)
- Optimize queries (2 days)
- Load testing (2 days)
- Total: 2 weeks work

---

## 📈 Load Testing Results (Estimated)

### Test 1: Problem Browsing
```
Current: 10-20 concurrent users
With Gunicorn: 100-200 concurrent users
With PostgreSQL: 500-1000 concurrent users
With CDN: 5000+ concurrent users
```

### Test 2: Code Submission
```
Current: 3-5 concurrent users (bottleneck)
With Gunicorn: 20-30 concurrent users
With Celery: 100-200 concurrent users
With Kubernetes: 1000+ concurrent users
```

### Test 3: Leaderboard
```
Current: 10-20 concurrent users
With Caching: 500-1000 concurrent users
With CDN: 5000+ concurrent users
```

---

## ✅ Final Recommendation

### For Development/Testing
**Current setup is OK**
- 3-5 concurrent users
- Good for demo
- No cost

### For Small Production (School/University)
**Use Gunicorn + PostgreSQL**
- 50-100 concurrent users
- $24-80/month
- 1 day setup

### For Medium Production (Startup)
**Use Celery + Redis + PostgreSQL**
- 500-1000 concurrent users
- $200-500/month
- 2 weeks setup

### For Large Production (Company)
**Use Kubernetes + Microservices**
- 10,000+ concurrent users
- $1000+/month
- 1-2 months setup

---

## 🎉 Summary

| Setup | Concurrent Users | Cost | Setup Time |
|-------|-----------------|------|------------|
| **Current (Dev)** | **3-5** | $0 | Ready |
| Gunicorn | 20-30 | $24 | 1 hour |
| + PostgreSQL | 50-100 | $80 | 1 day |
| + Celery | 500-1000 | $200 | 2 weeks |
| + Kubernetes | 10,000+ | $1000+ | 2 months |

**Javob:** Hozirgi holatda **3-5 ta foydalanuvchi** bir vaqtda kod yuborishi mumkin. Lekin oddiy browsing uchun **10-20 ta foydalanuvchi** ishlashi mumkin.

**Tavsiya:** Production uchun kamida Gunicorn + PostgreSQL ishlatish kerak (1 kun ichida sozlash mumkin).
