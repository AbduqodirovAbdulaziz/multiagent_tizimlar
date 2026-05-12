# PythonAnywhere Deployment - Console Buyruqlari

## 📋 Boshlash Oldin

**PythonAnywhere Console:** Bash console ochish
**Home Directory:** `/home/multiagent`

---

## 🚀 QADAMMA-QADAM DEPLOYMENT

### 1️⃣ Repository Clone Qilish

```bash
cd /home/multiagent
git clone https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git
cd multiagent_tizimlar
```

---

### 2️⃣ Virtual Environment Yaratish

```bash
# Python 3.10 bilan virtual environment
python3.10 -m venv venv

# Virtual environment faollashtirish
source venv/bin/activate
```

---

### 3️⃣ Dependencies O'rnatish

```bash
# Pip yangilash
pip install --upgrade pip

# Requirements o'rnatish
pip install -r requirements/prod.txt
```

**Agar xatolik bo'lsa, base.txt dan o'rnating:**
```bash
pip install -r requirements/base.txt
```

---

### 4️⃣ Environment Variables Sozlash

```bash
# .env fayl yaratish
nano .env
```

**`.env` fayliga quyidagilarni yozing:**
```env
# Django Settings
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com,localhost,127.0.0.1

# Database (SQLite for free tier)
DATABASE_URL=sqlite:///db.sqlite3

# Static files
STATIC_ROOT=/home/multiagent/multiagent_tizimlar/staticfiles
MEDIA_ROOT=/home/multiagent/multiagent_tizimlar/media

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**Ctrl+O** (saqlash), **Enter**, **Ctrl+X** (chiqish)

---

### 5️⃣ Production Settings Yaratish

```bash
# Production settings faylini yaratish
nano config/settings/prod.py
```

**`config/settings/prod.py` ga quyidagilarni yozing:**
```python
"""
Production settings for PythonAnywhere
"""
from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_ROOT = os.environ.get('STATIC_ROOT', BASE_DIR / 'staticfiles')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', BASE_DIR / 'media')
MEDIA_URL = '/media/'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Disable debug toolbar in production
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']
MIDDLEWARE = [mw for mw in MIDDLEWARE if 'debug_toolbar' not in mw]
```

**Ctrl+O**, **Enter**, **Ctrl+X**

---

### 6️⃣ Database Migrate

```bash
# Migratsiyalarni qo'llash
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (o'zingizning parolingiz)
```

---

### 7️⃣ Static Files Collect

```bash
# Static fayllarni yig'ish
python manage.py collectstatic --noinput
```

---

### 8️⃣ Demo Ma'lumotlarni Yuklash

```bash
# Kasallik naqshlari va demo bemorlarni yuklash
python manage.py load_sample_data
```

---

### 9️⃣ WSGI Fayl Yaratish

```bash
# WSGI fayl yaratish
nano /var/www/multiagent_pythonanywhere_com_wsgi.py
```

**WSGI fayliga quyidagilarni yozing:**
```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/multiagent/multiagent_tizimlar'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.prod'

# Activate virtual environment
activate_this = '/home/multiagent/multiagent_tizimlar/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Ctrl+O**, **Enter**, **Ctrl+X**

---

### 🔟 Test Qilish

```bash
# Django shell orqali test
python manage.py shell

# Shell ichida:
from apps.patients.models import Patient
from apps.diagnostics.models import DiseasePattern

print(f"Bemorlar: {Patient.objects.count()}")
print(f"Kasalliklar: {DiseasePattern.objects.count()}")

# Ctrl+D (chiqish)
```

---

## 🌐 PythonAnywhere Web Tab Sozlamalari

### Web Tab'da Quyidagilarni Sozlang:

1. **Source code:**
   ```
   /home/multiagent/multiagent_tizimlar
   ```

2. **Working directory:**
   ```
   /home/multiagent/multiagent_tizimlar
   ```

3. **WSGI configuration file:**
   ```
   /var/www/multiagent_pythonanywhere_com_wsgi.py
   ```

4. **Virtualenv:**
   ```
   /home/multiagent/multiagent_tizimlar/venv
   ```

5. **Static files:**
   - URL: `/static/`
   - Directory: `/home/multiagent/multiagent_tizimlar/staticfiles`

6. **Media files:**
   - URL: `/media/`
   - Directory: `/home/multiagent/multiagent_tizimlar/media`

---

## 🔄 Reload Web App

Web Tab'da **"Reload"** tugmasini bosing!

---

## ✅ Tekshirish

### 1. Web Saytni Ochish:
```
https://multiagent.pythonanywhere.com/
```

### 2. Admin Panel:
```
https://multiagent.pythonanywhere.com/admin/
```

### 3. API Docs (admin uchun):
```
https://multiagent.pythonanywhere.com/api/docs/
```

---

## 🐛 Muammolarni Hal Qilish

### Agar Static Files Ko'rinmasa:

```bash
cd /home/multiagent/multiagent_tizimlar
source venv/bin/activate
python manage.py collectstatic --noinput
```

Web Tab'da **Reload** qiling.

---

### Agar Database Xatosi Bo'lsa:

```bash
cd /home/multiagent/multiagent_tizimlar
source venv/bin/activate
python manage.py migrate
```

---

### Agar Import Xatosi Bo'lsa:

```bash
cd /home/multiagent/multiagent_tizimlar
source venv/bin/activate
pip install -r requirements/base.txt
```

---

### Error Log'larni Ko'rish:

PythonAnywhere Web Tab → **Error log** tugmasini bosing

---

## 📝 Yangilanishlarni Deploy Qilish

Keyinchalik GitHub'dan yangilanishlarni olish uchun:

```bash
cd /home/multiagent/multiagent_tizimlar
source venv/bin/activate

# Git pull
git pull origin main

# Dependencies yangilash (agar kerak bo'lsa)
pip install -r requirements/prod.txt

# Migrate
python manage.py migrate

# Static files
python manage.py collectstatic --noinput
```

Web Tab'da **Reload** qiling.

---

## 🎉 Tayyor!

Agar barcha qadamlar to'g'ri bajarilsa, sizning loyihangiz:

✅ https://multiagent.pythonanywhere.com/ da ishlaydi
✅ Admin panel: https://multiagent.pythonanywhere.com/admin/
✅ 15 ta kasallik naqshi
✅ 11 ta demo bemor
✅ To'liq ishlaydigan diagnostika tizimi

---

**Omad! 🚀**
