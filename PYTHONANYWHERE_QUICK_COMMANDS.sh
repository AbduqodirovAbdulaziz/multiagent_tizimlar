#!/bin/bash
# PythonAnywhere Quick Deployment Commands
# Copy-paste qilib ishlatish uchun

# ============================================
# 1. REPOSITORY CLONE
# ============================================
cd /home/multiagent
git clone https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git
cd multiagent_tizimlar

# ============================================
# 2. VIRTUAL ENVIRONMENT
# ============================================
python3.10 -m venv venv
source venv/bin/activate

# ============================================
# 3. DEPENDENCIES
# ============================================
pip install --upgrade pip
pip install -r requirements/base.txt

# ============================================
# 4. ENVIRONMENT VARIABLES
# ============================================
cat > .env << 'EOF'
DJANGO_SETTINGS_MODULE=config.settings.prod
SECRET_KEY=django-insecure-pythonanywhere-change-this-key-12345
DEBUG=False
ALLOWED_HOSTS=multiagent.pythonanywhere.com,localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
STATIC_ROOT=/home/multiagent/multiagent_tizimlar/staticfiles
MEDIA_ROOT=/home/multiagent/multiagent_tizimlar/media
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
EOF

# ============================================
# 5. PRODUCTION SETTINGS (agar yo'q bo'lsa)
# ============================================
# Agar config/settings/prod.py mavjud bo'lsa, o'tkazib yuboring
# Aks holda, dev.py dan foydalaning:
export DJANGO_SETTINGS_MODULE=config.settings.dev

# ============================================
# 6. DATABASE MIGRATE
# ============================================
python manage.py migrate

# ============================================
# 7. SUPERUSER (interaktiv)
# ============================================
echo "Superuser yaratish (username: admin, password: o'zingizniki):"
python manage.py createsuperuser

# ============================================
# 8. STATIC FILES
# ============================================
python manage.py collectstatic --noinput

# ============================================
# 9. DEMO DATA
# ============================================
python manage.py load_sample_data

# ============================================
# 10. TEST
# ============================================
python manage.py shell -c "from apps.patients.models import Patient; from apps.diagnostics.models import DiseasePattern; print(f'Bemorlar: {Patient.objects.count()}'); print(f'Kasalliklar: {DiseasePattern.objects.count()}')"

echo ""
echo "============================================"
echo "✅ DEPLOYMENT TAYYOR!"
echo "============================================"
echo ""
echo "Keyingi qadamlar:"
echo "1. PythonAnywhere Web Tab'ga o'ting"
echo "2. WSGI faylni sozlang"
echo "3. Static/Media papkalarni sozlang"
echo "4. Reload tugmasini bosing"
echo ""
echo "WSGI fayl yo'li: /var/www/multiagent_pythonanywhere_com_wsgi.py"
echo "Virtual env: /home/multiagent/multiagent_tizimlar/venv"
echo "Static: /home/multiagent/multiagent_tizimlar/staticfiles"
echo ""
