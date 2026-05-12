#!/bin/bash
# ============================================
# PYTHONANYWHERE DEPLOYMENT - BASH COMMANDS
# ============================================
# Bu buyruqlarni PythonAnywhere Bash console'ga
# ketma-ket copy-paste qiling
# ============================================

# ============================================
# 1. REPOSITORY CLONE (agar mavjud bo'lsa, o'tkazib yuboring)
# ============================================
cd ~
git clone https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git
cd multiagent_tizimlar

# ============================================
# 2. VIRTUAL ENVIRONMENT YARATISH
# ============================================
# PythonAnywhere'da mkvirtualenv ishlatamiz
mkvirtualenv --python=/usr/bin/python3.10 multiagent

# Virtual environment faollashtirish
workon multiagent

# ============================================
# 3. DEPENDENCIES O'RNATISH
# ============================================
pip install --upgrade pip
pip install -r requirements/base.txt

# Agar xatolik bo'lsa, alohida o'rnating:
# pip install Django==4.2.30
# pip install djangorestframework
# pip install django-jazzmin
# pip install drf-spectacular
# pip install django-cors-headers
# pip install whitenoise

# ============================================
# 4. ENVIRONMENT VARIABLES (.env fayl)
# ============================================
cat > .env << 'EOF'
# Django Settings
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere
SECRET_KEY=django-insecure-pythonanywhere-change-this-key-12345
DEBUG=False

# PythonAnywhere
PYTHONANYWHERE_USERNAME=multiagent

# Allowed Hosts
DJANGO_ALLOWED_HOSTS=multiagent.pythonanywhere.com,localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Static/Media
STATIC_ROOT=/home/multiagent/multiagent_tizimlar/staticfiles
MEDIA_ROOT=/home/multiagent/multiagent_tizimlar/media
EOF

# ============================================
# 5. LOGS PAPKASINI YARATISH
# ============================================
mkdir -p logs
touch logs/medical_mas.log
chmod 644 logs/medical_mas.log

# ============================================
# 6. DATABASE MIGRATE
# ============================================
python manage.py migrate --settings=config.settings.pythonanywhere

# ============================================
# 7. SUPERUSER YARATISH (interaktiv)
# ============================================
echo "Superuser yaratish:"
echo "Username: admin"
echo "Email: admin@example.com"
echo "Password: (o'zingizning xavfsiz parolingiz)"
python manage.py createsuperuser --settings=config.settings.pythonanywhere

# ============================================
# 8. STATIC FILES COLLECT
# ============================================
python manage.py collectstatic --noinput --settings=config.settings.pythonanywhere

# ============================================
# 9. DEMO MA'LUMOTLARNI YUKLASH
# ============================================
python manage.py load_sample_data --settings=config.settings.pythonanywhere

# ============================================
# 10. TEST QILISH
# ============================================
python manage.py check --settings=config.settings.pythonanywhere

# Database test
python manage.py shell --settings=config.settings.pythonanywhere << 'PYEOF'
from apps.patients.models import Patient
from apps.diagnostics.models import DiseasePattern
print(f"✓ Bemorlar: {Patient.objects.count()}")
print(f"✓ Kasalliklar: {DiseasePattern.objects.count()}")
PYEOF

# ============================================
# TAYYOR! Endi Web Tab'ni sozlang
# ============================================
echo ""
echo "============================================"
echo "✅ DEPLOYMENT TAYYOR!"
echo "============================================"
echo ""
echo "Keyingi qadamlar:"
echo "1. PythonAnywhere Web Tab'ga o'ting"
echo "2. 'Add a new web app' yoki mavjud app'ni sozlang"
echo "3. WSGI faylni sozlang (quyidagi ma'lumotlarni kiriting)"
echo "4. Static files mapping qo'shing"
echo "5. Reload tugmasini bosing"
echo ""
echo "WSGI Configuration:"
echo "  Source code: /home/multiagent/multiagent_tizimlar"
echo "  Virtualenv: /home/multiagent/.virtualenvs/multiagent"
echo "  Static URL: /static/"
echo "  Static Directory: /home/multiagent/multiagent_tizimlar/staticfiles"
echo ""
