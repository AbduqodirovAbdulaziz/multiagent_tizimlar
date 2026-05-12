# Medical MAS - Deployment Guide

## 🚀 PythonAnywhere Deployment

### Tezkor Boshlash

```bash
# 1. Clone repository
cd ~
git clone https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git
cd multiagent_tizimlar

# 2. Virtual environment
mkvirtualenv --python=/usr/bin/python3.10 multiagent
workon multiagent

# 3. Install dependencies
pip install -r requirements/base.txt

# 4. Environment variables
cat > .env << 'EOF'
DJANGO_SETTINGS_MODULE=config.settings.pythonanywhere
SECRET_KEY=your-secret-key-here
DEBUG=False
PYTHONANYWHERE_USERNAME=your-username
EOF

# 5. Database
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# 6. Load demo data
python manage.py load_sample_data
```

### Web Tab Configuration

1. **Source code:** `/home/your-username/multiagent_tizimlar`
2. **Virtualenv:** `/home/your-username/.virtualenvs/multiagent`
3. **WSGI file:** Use `pythonanywhere_wsgi.py` content
4. **Static files:** `/static/` → `/home/your-username/multiagent_tizimlar/staticfiles`

### Features

- ✅ 15 kasallik naqshi
- ✅ 11 demo bemor
- ✅ 5 ta agent (Symptom, Analysis, Diagnosis, Treatment, Coordinator)
- ✅ 39 simptom, 7 kategoriya
- ✅ Admin panel (Jazzmin)
- ✅ RESTful API
- ✅ API Documentation (Swagger)

## 📚 Documentation

- **README.md** - Asosiy hujjat
- **DEPLOYMENT_GUIDE.md** - Ushbu fayl
- **pythonanywhere_wsgi.py** - WSGI konfiguratsiya

## 🔗 Links

- **Repository:** https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar
- **Demo:** https://multiagent.pythonanywhere.com/ (coming soon)

---

**Version:** 2.0  
**Date:** 2026-05-12  
**Status:** Production Ready ✅
