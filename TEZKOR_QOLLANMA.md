# Tezkor Qo'llanma - Medical MAS

## 🚀 Serverni Ishga Tushirish

```bash
# Virtual environment faollashtirish
venv310\Scripts\activate

# Serverni ishga tushirish
python manage.py runserver 8080
```

Server manzili: **http://127.0.0.1:8080/**

## 📱 Asosiy Sahifalar

| Sahifa | URL | Tavsif |
|--------|-----|--------|
| Dashboard | http://127.0.0.1:8080/ | Asosiy sahifa, diagnostika qilish |
| Admin Panel | http://127.0.0.1:8080/admin/ | Bemorlar va sozlamalar |
| API Docs | http://127.0.0.1:8080/api/docs/ | API dokumentatsiya (admin) |
| Agent Status | http://127.0.0.1:8080/agents/ | Agentlar holati |

## 👤 Admin Ma'lumotlari

Agar admin parolini o'zgartirish kerak bo'lsa:

```bash
python manage.py changepassword admin
```

Yoki yangi superuser yaratish:

```bash
python manage.py createsuperuser
```

## 🏥 Bemor Qo'shish

1. Admin panelga kiring: http://127.0.0.1:8080/admin/
2. **"Patients"** bo'limini tanlang
3. **"Add Patient"** tugmasini bosing
4. Quyidagi ma'lumotlarni kiriting:

### Shaxsiy Ma'lumotlar:
- **Ism** (first_name)
- **Familiya** (last_name)
- **Otasining ismi** (middle_name)
- **Tug'ilgan sana** (date_of_birth)
- **Jins** (gender): Erkak/Ayol

### Tibbiy Ma'lumotlar:
- **Qon guruhi** (blood_type): A+, B+, O+, AB+, va boshqalar
- **Allergiyalar** (allergies): JSON format
  ```json
  ["Penitsil", "Yong'oq"]
  ```
- **Surunkali kasalliklar** (chronic_diseases): JSON format
  ```json
  ["Diabet", "Gipertoniya"]
  ```

### Aloqa Ma'lumotlari:
- **Telefon** (phone)
- **Email** (email)
- **Manzil** (address)
- **Favqulodda aloqa** (emergency_contact)

5. **"Save"** tugmasini bosing

## 🔬 Diagnostika Qilish

### 1-Qadam: Dashboard'ga O'tish
http://127.0.0.1:8080/ sahifasini oching

### 2-Qadam: Bemorni Tanlash
"Yangi Diagnostika Boshlash" formasida bemorni dropdown'dan tanlang

### 3-Qadam: Simptomlarni Tanlash
Quyidagi kategoriyalardan kerakli simptomlarni checkbox orqali belgilang:

#### Umumiy Simptomlar:
- [ ] Isitma
- [ ] Charchoq
- [ ] Ishtahasizlik
- [ ] Vazn yo'qotish
- [ ] Terlash
- [ ] Titroq

#### Nafas Olish Tizimi:
- [ ] Yo'tal
- [ ] Nafas qisilishi
- [ ] Burun bitishi
- [ ] Tomoq og'rig'i
- [ ] Ko'krak og'rig'i
- [ ] Xirillash

#### Ovqat Hazm Qilish:
- [ ] Qorin og'rig'i
- [ ] Ko'ngil aynishi
- [ ] Qusish
- [ ] Ichburug'
- [ ] Qabziyat
- [ ] Oshqozon og'rig'i

#### Asab Tizimi:
- [ ] Bosh og'rig'i
- [ ] Bosh aylanishi
- [ ] Hushidan ketish
- [ ] Uyqusizlik
- [ ] Xotira zaiflanishi
- [ ] Qo'l-oyoq uyushishi

#### Yurak-Qon Tomir:
- [ ] Yurak urishi
- [ ] Ko'krak og'rig'i
- [ ] Nafas qisilishi
- [ ] Oyoq shishishi
- [ ] Qon bosimi o'zgarishi

#### Mushak-Skelet:
- [ ] Bo'g'im og'rig'i
- [ ] Mushak og'rig'i
- [ ] Orqa og'rig'i
- [ ] Bo'yin og'rig'i
- [ ] Harakatsizlik

#### Teri:
- [ ] Toshmalar
- [ ] Qichishish
- [ ] Teri qizarishi
- [ ] Shish
- [ ] Teri rangi o'zgarishi

### 4-Qadam: Harorat (Ixtiyoriy)
Agar bemor harorati o'lchangan bo'lsa, kiriting (masalan: 38.5)

### 5-Qadam: Diagnostika Boshlash
**"🚀 Diagnostika Boshlash"** tugmasini bosing

### 6-Qadam: Natijalarni Ko'rish
Tizim avtomatik ravishda natijalar sahifasiga yo'naltiradi

## 📊 Natijalarni Tushunish

### Diagnostika Natijasi:
- **Kasallik nomi**: Aniqlangan kasallik
- **Ishonch darajasi**: 0-100% (qanchalik yuqori bo'lsa, shunchalik aniq)
- **Og'irlik darajasi**: PAST, O'RTA, YUQORI, KRITIK
- **Tavsif**: Kasallik haqida ma'lumot
- **Davolash rejasi**: Tavsiya etilgan davolash

### Misol:
```
Kasallik: Gripp
Ishonch darajasi: 85.5%
Og'irlik: O'RTA
Tavsif: Virusli infeksiya...
Davolash rejasi: Dam olish, ko'p suyuqlik ichish...
```

## 🤖 Agent Jarayoni

Diagnostika paytida quyidagi agentlar ishga tushadi:

1. **SymptomAgent** 🔍
   - Simptomlarni tahlil qiladi
   - Kategoriyalarga ajratadi
   - Og'irlik darajasini aniqlaydi

2. **AnalysisAgent** 🧪
   - Tibbiy tahlillarni baholaydi
   - Test natijalarini tahlil qiladi

3. **DiagnosisAgent** 🏥
   - Kasallik diagnozini aniqlaydi
   - Ishonch darajasini hisoblaydi
   - Kasallik naqshlari bilan solishtiradi

4. **TreatmentAgent** 💊
   - Davolash rejasini taklif qiladi
   - Dori-darmonlarni tavsiya qiladi
   - Oldini olish choralarini ko'rsatadi

5. **CoordinatorAgent** 🎯
   - Barcha agentlarni muvofiqlashtiradi
   - Jarayonni boshqaradi
   - Natijalarni yig'adi

## 🗄️ Database Ma'lumotlari

### Joriy Holat:
- **Bemorlar:** 1 faol
- **Kasallik Naqshlari:** 5 ta
  - Gripp
  - Bronxit
  - Gastrit
  - Migren
  - Shamollash (ORVI)
- **Agentlar:** 5 ta
- **Sessiyalar:** 2 ta

### Database Tozalash:
Agar test ma'lumotlarni o'chirish kerak bo'lsa:

```bash
python clear_demo_data.py
```

## 🛠️ Foydali Komandalar

### Migratsiyalar:
```bash
# Yangi migratsiya yaratish
python manage.py makemigrations

# Migratsiyalarni qo'llash
python manage.py migrate
```

### Static Fayllar:
```bash
# Static fayllarni yig'ish
python manage.py collectstatic --noinput
```

### Shell:
```bash
# Django shell
python manage.py shell

# Bemorlarni ko'rish
from apps.patients.models import Patient
Patient.objects.all()
```

### Test:
```bash
# Dashboard flow test
python test_dashboard_flow.py

# Pytest
pytest
```

## ❓ Tez-Tez So'raladigan Savollar

### 1. Bemor qo'sha olmayman?
**Javob:** Bemorlarni faqat admin paneldan qo'shish mumkin. Dashboard'da faqat mavjud bemorlarni tanlash mumkin.

### 2. API dokumentatsiyani ko'ra olmayman?
**Javob:** API docs faqat admin/staff foydalanuvchilar uchun ochiq. Admin sifatida kirish kerak.

### 3. Simptomlarni qanday kiritaman?
**Javob:** Simptomlarni checkbox orqali tanlang. Textarea yo'q, faqat checkbox'lar.

### 4. Natijalar noto'g'ri chiqyapti?
**Javob:** Kasallik naqshlarini admin panelda tekshiring. Simptomlar to'g'ri kiritilganligiga ishonch hosil qiling.

### 5. Server ishlamayapti?
**Javob:** 
```bash
# Virtual environment faollashtiring
venv310\Scripts\activate

# Serverni qayta ishga tushiring
python manage.py runserver 8080
```

## 📞 Yordam

Agar muammo yuzaga kelsa:

1. **Loglarni tekshiring:** `logs/medical_mas.log`
2. **Database tekshiring:** Admin panelda ma'lumotlarni ko'ring
3. **Test qiling:** `python test_dashboard_flow.py`
4. **Qayta ishga tushiring:** Serverni to'xtatib, qayta ishga tushiring

## 📚 Qo'shimcha Hujjatlar

- `README.md` - Asosiy dokumentatsiya
- `DASHBOARD_IMPROVEMENTS_COMPLETE.md` - Dashboard yaxshilanishlari
- `FINAL_IMPLEMENTATION_SUMMARY.md` - To'liq implementatsiya hisoboti
- `SERVER_RUNNING_GUIDE.md` - Server ishga tushirish qo'llanmasi
- `PYTHONANYWHERE_DEPLOYMENT.md` - PythonAnywhere deployment

---
**Muallif:** Medical MAS Team  
**Sana:** 2026-05-12  
**Versiya:** 2.0  
**Status:** Tayyor ✅
