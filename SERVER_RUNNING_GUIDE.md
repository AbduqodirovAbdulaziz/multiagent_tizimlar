# Medical Multiagent System - Server Ishga Tushirildi! 🚀

**Sana:** 12-May, 2026  
**Holat:** ✅ SERVER ISHLAYAPTI

---

## ✅ Server Muvaffaqiyatli Ishga Tushdi!

```
Django version 4.2.30, using settings 'config.settings.dev'
Starting development server at http://127.0.0.1:8080/
Quit the server with CTRL-BREAK.
```

---

## 🌐 Kirish Manzillari

### 1. Admin Panel
```
URL: http://127.0.0.1:8080/admin/
Username: admin
Password: admin123
```

**Mavjud Bo'limlar:**
- ✅ Bemorlar (Patients)
- ✅ Simptomlar (Symptoms)
- ✅ Tibbiy Tarix (Medical History)
- ✅ Kasalliklar (Disease Patterns)
- ✅ Diagnostika Sessiyalari (Diagnostic Sessions)
- ✅ Diagnostika Natijalari (Diagnostic Results)
- ✅ Agent Holatlari (Agent States)
- ✅ Agent Loglar (Agent Logs)
- ✅ ACL Xabarlar (ACL Messages)

### 2. Dashboard
```
URL: http://127.0.0.1:8080/
```

**Xususiyatlar:**
- Statistika
- So'nggi sessiyalar
- Agent holatlari

### 3. API Documentation
```
Swagger UI: http://127.0.0.1:8080/api/docs/
ReDoc: http://127.0.0.1:8080/api/redoc/
Schema: http://127.0.0.1:8080/api/schema/
```

### 4. API Endpoints
```
Base URL: http://127.0.0.1:8080/api/v1/

Patients: /api/v1/patients/
Symptoms: /api/v1/symptoms/
Medical History: /api/v1/medical-history/
Diseases: /api/v1/diseases/
Diagnostics: /api/v1/diagnostics/
Agents: /api/v1/agents/
Agent Logs: /api/v1/agent-logs/
ACL Messages: /api/v1/acl-messages/
```

### 5. Web Pages
```
Bemorlar: http://127.0.0.1:8080/patients/
Diagnostika: http://127.0.0.1:8080/diagnostics/
Agentlar: http://127.0.0.1:8080/agents/
```

---

## 🧪 Tezkor Test

### 1. Admin Panel Tekshirish

1. Brauzerda oching: http://127.0.0.1:8080/admin/
2. Login qiling: admin / admin123
3. "Patients" bo'limiga kiring
4. Yangi bemor qo'shing:
   - Ism: Ali
   - Familiya: Valiyev
   - Tug'ilgan sana: 1990-01-01
   - Jins: Erkak
   - Telefon: +998901234567

### 2. Diagnostika Testi

#### API orqali (Postman yoki curl):

```bash
# 1. Token olish (agar kerak bo'lsa)
curl -X POST http://127.0.0.1:8080/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 2. Diagnostika sessiyasi yaratish
curl -X POST http://127.0.0.1:8080/api/v1/diagnostics/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "patient_id": 1,
    "symptoms": ["isitma", "bosh og'\''rig'\''i", "yo'\''tal"],
    "test_results": {"temperature": 38.5}
  }'
```

#### Python orqali:

```python
# Terminal'da
python test_diagnostic_flow.py
```

### 3. Dashboard Tekshirish

1. Oching: http://127.0.0.1:8080/
2. Statistikani ko'ring
3. So'nggi sessiyalarni ko'ring
4. Agent holatlarini tekshiring

---

## 📊 Mavjud Ma'lumotlar

### Database:
```
Location: db.sqlite3
Type: SQLite
```

### Sample Data:
```bash
# Sample data yuklash
python manage.py load_sample_data
```

**Yuklanadigan ma'lumotlar:**
- 5 ta kasallik naqshi (Disease Patterns)
- Simptomlar ro'yxati
- Tavsiya etilgan tahlillar

---

## 🔧 Server Boshqaruvi

### Server To'xtatish:
```bash
# Terminal'da
CTRL + C
```

### Server Qayta Ishga Tushirish:
```bash
python manage.py runserver 8080
```

### Boshqa Portda Ishga Tushirish:
```bash
python manage.py runserver 8000
```

### Barcha Interfacelar Uchun:
```bash
python manage.py runserver 0.0.0.0:8080
```

---

## 🐛 Muammolarni Hal Qilish

### Muammo 1: Port Band
```
Error: That port is already in use.
```

**Yechim:**
```bash
# Boshqa port ishlatilng
python manage.py runserver 8000
```

### Muammo 2: Migration Xatoligi
```
Error: No such table
```

**Yechim:**
```bash
python manage.py migrate
```

### Muammo 3: Static Files Yo'q
```
Error: Static files not found
```

**Yechim:**
```bash
python manage.py collectstatic --noinput
```

### Muammo 4: Admin Login Qila Olmayapti
```
Error: Invalid credentials
```

**Yechim:**
```bash
# Yangi superuser yaratish
python manage.py createsuperuser

# Yoki parolni o'zgartirish
python set_admin_password.py
```

---

## 📝 Foydali Buyruqlar

### Database:
```bash
# Database shell
python manage.py dbshell

# Django shell
python manage.py shell
```

### Migrations:
```bash
# Yangi migration yaratish
python manage.py makemigrations

# Migration qo'llash
python manage.py migrate

# Migration holatini ko'rish
python manage.py showmigrations
```

### Testing:
```bash
# Django testlar
python manage.py test

# Custom testlar
python test_diagnostic_flow.py
python test_logic_flow.py
```

### Logs:
```bash
# Log faylni ko'rish
cat logs/medical_mas.log

# Real-time log
tail -f logs/medical_mas.log
```

---

## 🎯 Keyingi Qadamlar

### 1. Ma'lumotlar Kiritish

**Admin Panel orqali:**
1. Bemorlar qo'shing
2. Kasallik naqshlarini kiriting
3. Simptomlarni qo'shing

**Sample Data orqali:**
```bash
python manage.py load_sample_data
```

### 2. Diagnostika Testi

**Test script orqali:**
```bash
python test_diagnostic_flow.py
```

**API orqali:**
- Swagger UI'dan foydalaning
- Postman'da test qiling

### 3. Agent Monitoring

**Dashboard:**
- http://127.0.0.1:8080/agents/

**Admin Panel:**
- Agent States
- Agent Logs
- ACL Messages

### 4. GitHub'ga Yuklash

```bash
git add .
git commit -m "Final version with all improvements"
git push origin main
```

### 5. PythonAnywhere'ga Deploy

`PYTHONANYWHERE_DEPLOYMENT.md` faylini o'qing

---

## 📊 Tizim Holati

### ✅ Ishlayotgan Komponentlar:

- ✅ Django Server (8080 port)
- ✅ SQLite Database
- ✅ Admin Panel
- ✅ API Endpoints
- ✅ Dashboard
- ✅ 5 AI Agents
- ✅ Agent Coordination
- ✅ Logging System

### 📈 Statistika:

- **Django Apps:** 6
- **Models:** 10+
- **API Endpoints:** 25+
- **Admin Interfaces:** 8
- **Agents:** 5
- **Templates:** 4

---

## 🎨 Admin Panel Xususiyatlari

### Mavjud Funksiyalar:

1. **Bemorlar Boshqaruvi**
   - Bemor qo'shish/tahrirlash
   - Simptomlar inline
   - Tibbiy tarix inline
   - BMI va yosh avtomatik hisoblash

2. **Kasalliklar Bazasi**
   - Kasallik naqshlari
   - Simptomlar ro'yxati
   - Tavsiya etilgan tahlillar
   - Davolash variantlari

3. **Diagnostika Sessiyalari**
   - Sessiya yaratish (API orqali)
   - Natijalarni ko'rish
   - Agent holatlarini kuzatish
   - Davomiylikni ko'rish

4. **Agent Monitoring**
   - Agent holatlari
   - Agent loglar
   - ACL xabarlar
   - Real-time monitoring

5. **Qidirish va Filtrlash**
   - Ism, familiya bo'yicha
   - Telefon, email bo'yicha
   - Sana oralig'i bo'yicha
   - Status bo'yicha

---

## 💡 Maslahatlar

1. **Development:**
   - DEBUG=True qoldiring
   - Log'larni kuzatib boring
   - Test'larni muntazam ishga tushiring

2. **Ma'lumotlar:**
   - Sample data yuklang
   - Test bemorlar yarating
   - Kasallik naqshlarini to'ldiring

3. **Testing:**
   - Har bir o'zgarishdan keyin test qiling
   - API'ni Swagger'da sinab ko'ring
   - Admin panel'ni tekshiring

4. **Monitoring:**
   - Agent loglarni ko'ring
   - Session holatlarini kuzating
   - Xatolarni tezda toping

5. **Backup:**
   - Database'ni muntazam backup oling
   - Git'ga commit qiling
   - .env faylini himoyalang

---

## 🎉 Muvaffaqiyat!

Server muvaffaqiyatli ishga tushdi va to'liq ishlayapti!

**Kirish:**
- Admin: http://127.0.0.1:8080/admin/
- Dashboard: http://127.0.0.1:8080/
- API Docs: http://127.0.0.1:8080/api/docs/

**Login:**
- Username: admin
- Password: admin123

---

**Yaratilgan:** 12-May, 2026  
**Server:** http://127.0.0.1:8080/  
**Holat:** ✅ ISHLAYAPTI

**Omad tilaymiz! 🚀**
