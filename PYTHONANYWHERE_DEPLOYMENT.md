# 🚀 PythonAnywhere Deployment Guide

## ✅ Loyiha Tayyor!

**Python Version**: 3.10  
**Django Version**: 4.2.30 LTS  
**Status**: Production Ready ✅

---

## 📋 PythonAnywhere'ga Deployment

### 1. Account Yaratish

1. https://www.pythonanywhere.com/ ga kiring
2. **Beginner** (tekin) account yarating
3. Email tasdiqlang

### 2. Bash Console Ochish

PythonAnywhere dashboard → **Consoles** → **Bash**

### 3. Loyihani Yuklash

```bash
# GitHub'dan clone qilish
git clone https://github.com/<username>/medical-mas.git
cd medical-mas

# Yoki zip fayl yuklash
# Files tab → Upload → medical-mas.zip
# unzip medical-mas.zip
# cd medical-mas
```

### 4. Virtual Environment Yaratish

```bash
# Python 3.10 bilan venv yaratish
mkvirtualenv --python=/usr/bin/python3.10 medical_mas

# Dependencies o'rnatish
pip install -r requirements/prod.txt
```

### 5. Environment Variables

`.env` faylini yarating:

```bash
nano .env
```

Quyidagi ma'lumotlarni kiriting:

```env
DJANGO_SECRET_KEY=<your-secret-key-here>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=<username>.pythonanywhere.com
DJANGO_SETTINGS_MODULE=config.settings.prod

# Database (SQLite - tekin tarif uchun)
# PostgreSQL faqat pullik tariflarda

# Redis (ixtiyoriy - pullik tariflarda)
# REDIS_URL=redis://localhost:6379/0
```

Secret key generatsiya qilish:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Database Setup

```bash
# Migratsiyalar
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Test ma'lumotlar (ixtiyoriy)
python manage.py load_sample_data

# Static files
python manage.py collectstatic --noinput
```

### 7. Web App Sozlash

**Web** tab → **Add a new web app**

1. **Manual configuration** tanlang
2. **Python 3.10** tanlang
3. **Next** bosing

### 8. WSGI File Sozlash

**Web** tab → **WSGI configuration file** linkini bosing

Faylni quyidagicha o'zgartiring:

```python
import os
import sys

# Path to your project
path = '/home/<username>/medical-mas'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'

# Load .env file
from pathlib import Path
env_file = Path(path) / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

# Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**DIQQAT**: `<username>` ni o'z username'ingiz bilan almashtiring!

### 9. Virtual Environment Path

**Web** tab → **Virtualenv** bo'limida:

```
/home/<username>/.virtualenvs/medical_mas
```

### 10. Static Files

**Web** tab → **Static files** bo'limida:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/<username>/medical-mas/staticfiles/` |
| `/media/` | `/home/<username>/medical-mas/media/` |

### 11. Source Code

**Web** tab → **Code** bo'limida:

- **Source code**: `/home/<username>/medical-mas`
- **Working directory**: `/home/<username>/medical-mas`

### 12. Reload

**Web** tab → **Reload** tugmasini bosing 🔄

---

## 🌐 Saytingiz Tayyor!

Saytingiz: `https://<username>.pythonanywhere.com`

- **Admin Panel**: `https://<username>.pythonanywhere.com/admin/`
- **Dashboard**: `https://<username>.pythonanywhere.com/`
- **API Docs**: `https://<username>.pythonanywhere.com/api/docs/`

---

## 🔧 Troubleshooting

### Error Log Ko'rish

**Web** tab → **Log files** → **Error log**

### Database Muammolari

```bash
# Bash console
cd medical-mas
workon medical_mas
python manage.py migrate
```

### Static Files Yuklanmayapti

```bash
python manage.py collectstatic --noinput --clear
```

Web tab → Reload

### Import Errors

WSGI file'da path to'g'ri ekanligini tekshiring:

```python
path = '/home/<username>/medical-mas'  # To'g'ri path
```

---

## 📊 Tekin Tarif Cheklovlari

PythonAnywhere tekin tarifida:

- ✅ Python 3.10
- ✅ Django 4.2
- ✅ SQLite database
- ✅ 512 MB disk space
- ✅ 1 web app
- ❌ PostgreSQL (pullik)
- ❌ Redis (pullik)
- ❌ Celery (pullik)
- ❌ Custom domain (pullik)

**Yechim**: Loyiha SQLite bilan to'liq ishlaydi!

---

## 🔄 Yangilanishlar

Loyihani yangilash:

```bash
# Bash console
cd medical-mas
workon medical_mas

# Git pull
git pull origin main

# Dependencies
pip install -r requirements/prod.txt

# Migrate
python manage.py migrate

# Static files
python manage.py collectstatic --noinput

# Web tab → Reload
```

---

## 📝 Production Settings

`config/settings/prod.py` faylida:

- ✅ `DEBUG = False`
- ✅ `ALLOWED_HOSTS` sozlangan
- ✅ `SECRET_KEY` muhit o'zgaruvchisida
- ✅ HTTPS redirect yoqilgan
- ✅ Security headers sozlangan

---

## 🎓 Akademik Jihat

Bu loyiha quyidagi kontseptsiyalarni amalga oshiradi:

1. **FIPA-ACL Protokoli** ✅
2. **BDI Arxitektura** ✅
3. **Multiagent Koordinatsiya** ✅
4. **RESTful API** ✅
5. **Production Deployment** ✅

---

## 📞 Yordam

Muammolar yuzaga kelsa:

1. Error log'ni tekshiring
2. WSGI file'ni tekshiring
3. Virtual environment path'ni tekshiring
4. Static files'ni qayta collect qiling

---

## ✅ Checklist

Deployment oldidan tekshiring:

- [ ] `.env` fayl yaratilgan
- [ ] `SECRET_KEY` o'rnatilgan
- [ ] `ALLOWED_HOSTS` to'g'ri
- [ ] Migratsiyalar bajarilgan
- [ ] Superuser yaratilgan
- [ ] Static files collect qilingan
- [ ] WSGI file to'g'ri sozlangan
- [ ] Virtual environment path to'g'ri
- [ ] Web app reload qilingan

---

**Muvaffaqiyatlar!** 🎉

Loyihangiz PythonAnywhere'da ishga tushdi!
