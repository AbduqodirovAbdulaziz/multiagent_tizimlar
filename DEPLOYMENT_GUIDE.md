# Medical MAS - Deployment Guide

## 🚀 Loyihani Ishga Tushirish

### 1. Lokal Development

```bash
# Virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Dependencies
pip install -r requirements/dev.txt

# Migratsiyalar
python manage.py migrate

# Superuser
python manage.py createsuperuser

# Test malumotlar
python manage.py load_sample_data

# Server
python manage.py runserver 8080
```

### 2. Admin Panel

- URL: http://127.0.0.1:8080/admin/
- Username: admin
- Password: admin123

### 3. Dashboard

- URL: http://127.0.0.1:8080/

### 4. API Documentation

- Swagger UI: http://127.0.0.1:8080/api/docs/
- ReDoc: http://127.0.0.1:8080/api/redoc/

## 📦 PythonAnywhere Deployment

### 1. Fayllarni Yuklash

```bash
# Git orqali
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. PythonAnywhere Setup

1. **Account yaratish**: https://www.pythonanywhere.com/
2. **Bash console** ochish
3. **Loyihani clone qilish**:

```bash
git clone <your-repo-url>
cd MULTIAGENT
```

4. **Virtual environment**:

```bash
mkvirtualenv --python=/usr/bin/python3.11 medical_mas
pip install -r requirements/prod.txt
```

5. **Web app sozlash**:
   - Web tab → Add a new web app
   - Manual configuration → Python 3.11
   - Virtualenv: `/home/<username>/.virtualenvs/medical_mas`
   - Source code: `/home/<username>/MULTIAGENT`
   - Working directory: `/home/<username>/MULTIAGENT`

6. **WSGI file** (`/var/www/<username>_pythonanywhere_com_wsgi.py`):

```python
import os
import sys

path = '/home/<username>/MULTIAGENT'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

7. **Static files**:

```bash
python manage.py collectstatic --noinput
```

PythonAnywhere Web tab:
- Static files URL: `/static/`
- Static files directory: `/home/<username>/MULTIAGENT/staticfiles/`

8. **Database**:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_data
```

9. **Environment variables**:

`.env` faylini yarating:

```bash
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<username>.pythonanywhere.com
```

10. **Reload** web app

## 🔧 Production Settings

### Security Checklist

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` muhit o'zgaruvchisida
- [ ] `ALLOWED_HOSTS` to'g'ri sozlangan
- [ ] HTTPS yoqilgan
- [ ] Database backup sozlangan
- [ ] Error logging (Sentry) sozlangan

### Environment Variables

```bash
# Production
DJANGO_SECRET_KEY=<random-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://localhost:6379/0
```

## 📊 Monitoring

### Logs

```bash
# Django logs
tail -f logs/medical_mas.log

# PythonAnywhere error log
# Web tab → Log files → Error log
```

### Health Check

```bash
curl http://yourdomain.com/health/
```

## 🔄 Updates

```bash
# Pull changes
git pull origin main

# Install dependencies
pip install -r requirements/prod.txt

# Migrate
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput

# Reload (PythonAnywhere)
# Web tab → Reload button
```

## 🐛 Troubleshooting

### Import Errors

```bash
# Check Python path
python manage.py shell
>>> import sys
>>> print(sys.path)
```

### Static Files Not Loading

```bash
# Collect static again
python manage.py collectstatic --noinput --clear

# Check STATIC_ROOT
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_ROOT)
```

### Database Connection Error

```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Test connection
python manage.py dbshell
```

## 📚 API Usage Examples

### Create Diagnostic Session

```bash
curl -X POST http://localhost:8080/api/v1/diagnostics/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{
    "patient_id": 1,
    "symptoms": ["bosh ogrigi", "isitma", "yotal"],
    "test_results": {"temperature": 38.5}
  }'
```

### Get Session Status

```bash
curl http://localhost:8080/api/v1/diagnostics/1/status/ \
  -H "Authorization: Token <your-token>"
```

### Get Results

```bash
curl http://localhost:8080/api/v1/diagnostics/1/results/ \
  -H "Authorization: Token <your-token>"
```

## 🎓 Akademik Jihat

### Multiagent Tizim Arxitekturasi

Bu loyiha quyidagi MAS kontseptsiyalarini amalga oshiradi:

1. **FIPA-ACL Protokoli**: Standart agent kommunikatsiya tili
2. **BDI Modeli**: Belief-Desire-Intention agent arxitekturasi
3. **Koordinatsiya**: Markaziy koordinator pattern
4. **Parallel Execution**: Celery orqali asinxron bajarish
5. **Message Queue**: Redis Pub/Sub

### Foydalanilgan Texnologiyalar

- **Django 6.0**: Web framework
- **DRF**: RESTful API
- **Celery**: Asinxron task queue
- **Redis**: Cache va message broker
- **PostgreSQL/SQLite**: Database
- **Jazzmin**: Admin theme

## 📞 Support

Muammolar yuzaga kelsa:
- GitHub Issues: <your-repo-url>/issues
- Email: support@medical-mas.uz

---

**Medical MAS** © 2024 - Multiagent Tibbiy Diagnostika Platformasi
