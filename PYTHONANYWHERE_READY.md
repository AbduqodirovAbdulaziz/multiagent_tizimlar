# ✅ PythonAnywhere Deployment - TAYYOR!

## 🎯 Sizga Kerakli Fayllar

Barcha kerakli fayllar GitHub'ga yuklandi va tayyor!

**Repository:** https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar

---

## 📁 Deployment Fayllari

### 1. **COPY_PASTE_COMMANDS.txt** ⭐ ENG OSON
   - Oddiy copy-paste buyruqlar
   - Har bir qadam alohida
   - Tushuntirish bilan
   - **Boshlang'ichlar uchun eng yaxshi!**

### 2. **PYTHONANYWHERE_COMMANDS.md** 📖 BATAFSIL
   - To'liq qo'llanma
   - Har bir qadam tushuntirilgan
   - Troubleshooting bo'limi
   - Web Tab sozlamalari

### 3. **PYTHONANYWHERE_QUICK_COMMANDS.sh** 🚀 AVTOMATIK
   - Bash skript
   - Avtomatik deployment
   - Bir nechta buyruq bilan
   - **Tajribali foydalanuvchilar uchun**

### 4. **pythonanywhere_wsgi.py** ⚙️ WSGI CONFIG
   - WSGI konfiguratsiya fayli
   - Copy-paste qilish uchun tayyor
   - PythonAnywhere Web Tab uchun

---

## 🚀 TEZKOR BOSHLASH

### PythonAnywhere Console'da:

```bash
# 1. Repository clone
cd /home/multiagent
git clone https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar.git
cd multiagent_tizimlar

# 2. Virtual environment
python3.10 -m venv venv
source venv/bin/activate

# 3. Dependencies
pip install --upgrade pip
pip install -r requirements/base.txt

# 4. Database
python manage.py migrate

# 5. Superuser
python manage.py createsuperuser

# 6. Static files
python manage.py collectstatic --noinput

# 7. Demo data
python manage.py load_sample_data

# 8. Test
python manage.py shell -c "from apps.patients.models import Patient; print(f'Bemorlar: {Patient.objects.count()}')"
```

---

## 🌐 Web Tab Sozlamalari

### PythonAnywhere Web Tab'da:

1. **Source code:**
   ```
   /home/multiagent/multiagent_tizimlar
   ```

2. **Virtualenv:**
   ```
   /home/multiagent/multiagent_tizimlar/venv
   ```

3. **WSGI file:** (linkni bosing va quyidagini yozing)
   ```python
   import os
   import sys
   
   project_home = '/home/multiagent/multiagent_tizimlar'
   if project_home not in sys.path:
       sys.path.insert(0, project_home)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.dev'
   
   venv_site_packages = '/home/multiagent/multiagent_tizimlar/venv/lib/python3.10/site-packages'
   if venv_site_packages not in sys.path:
       sys.path.insert(0, venv_site_packages)
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

4. **Static files:**
   - URL: `/static/`
   - Directory: `/home/multiagent/multiagent_tizimlar/staticfiles`

5. **Reload** tugmasini bosing!

---

## ✅ Natija

Agar hammasi to'g'ri bo'lsa:

- ✅ **Web sayt:** https://multiagent.pythonanywhere.com/
- ✅ **Admin panel:** https://multiagent.pythonanywhere.com/admin/
- ✅ **API docs:** https://multiagent.pythonanywhere.com/api/docs/
- ✅ **15 ta kasallik naqshi**
- ✅ **11 ta demo bemor**
- ✅ **To'liq ishlaydigan diagnostika tizimi**

---

## 📚 Qo'shimcha Hujjatlar

Repository'da quyidagi fayllar mavjud:

- `PYTHONANYWHERE_DEPLOYMENT.md` - Eski deployment qo'llanmasi
- `README.md` - Loyiha haqida
- `TEZKOR_QOLLANMA.md` - Tezkor qo'llanma
- `YAKUNIY_XULOSA.md` - Yakuniy xulosa

---

## 🐛 Muammolar?

### Error Log Ko'rish:
PythonAnywhere Web Tab → **Error log** tugmasi

### Console'da Test:
```bash
cd /home/multiagent/multiagent_tizimlar
source venv/bin/activate
python manage.py check
```

### Static Files Qayta Yig'ish:
```bash
python manage.py collectstatic --noinput
```

### Reload:
Web Tab'da **Reload** tugmasi

---

## 🔄 Yangilanishlar

Keyinchalik GitHub'dan yangilanishlarni olish:

```bash
cd /home/multiagent/multiagent_tizimlar
source venv/bin/activate
git pull origin main
pip install -r requirements/base.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Web Tab'da **Reload**

---

## 📞 Yordam

Agar muammo bo'lsa:

1. **Error log'ni tekshiring**
2. **Console'da `python manage.py check` bajaring**
3. **PYTHONANYWHERE_COMMANDS.md faylini o'qing**
4. **COPY_PASTE_COMMANDS.txt dan foydalaning**

---

## 🎉 Omad!

Barcha kerakli fayllar tayyor va GitHub'da!

**Keyingi qadam:** PythonAnywhere console'ga o'ting va deployment'ni boshlang!

---

**Repository:** https://github.com/AbduqodirovAbdulaziz/multiagent_tizimlar  
**Sana:** 2026-05-12  
**Status:** ✅ TAYYOR
