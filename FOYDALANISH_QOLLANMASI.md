# 🏥 Medical MAS - Foydalanish Qo'llanmasi

## Loyiha Haqida

**Medical MAS** - Multiagent Tibbiy Diagnostika Platformasi. Bu tizim 5 ta maxsus agent yordamida bemorlarni diagnostika qiladi va davolash rejasini taklif qiladi.

### Texnologiyalar
- **Backend**: Django 4.2.30 LTS
- **Python**: 3.10.1
- **Database**: SQLite3
- **Admin Panel**: Django Jazzmin
- **API**: Django REST Framework

---

## 🚀 Serverni Ishga Tushirish

### 1. Virtual Environment Aktivlashtirish

**Windows (PowerShell):**
```powershell
.\venv310\Scripts\activate
```

**Windows (CMD):**
```cmd
venv310\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv310/bin/activate
```

### 2. Serverni Ishga Tushirish

```bash
python manage.py runserver 8080
```

Server manzili: **http://127.0.0.1:8080/**

---

## 📋 Tizimdan Foydalanish

### 1. Admin Panel

**Manzil**: http://127.0.0.1:8080/admin/

**Login ma'lumotlari**:
- Username: `admin`
- Password: `admin123`

#### Admin Panelda Nima Qilish Mumkin?

✅ **Bemorlarni boshqarish** (`Patients`)
- Yangi bemor qo'shish
- Bemor ma'lumotlarini tahrirlash
- Bemorlar ro'yxatini ko'rish

✅ **Kasalliklarni boshqarish** (`Disease Patterns`)
- Yangi kasallik qo'shish
- Kasallik simptomlarini belgilash
- Tavsiya etiladigan tahlillarni kiritish

✅ **Diagnostika sessiyalarini ko'rish** (`Diagnostic Sessions`)
- Barcha diagnostika sessiyalari
- Har bir sessiya detallari
- Agent holatlari

✅ **Natijalarni ko'rish** (`Diagnostic Results`)
- Diagnostika natijalari
- Ishonch darajasi
- Davolash rejalari

✅ **Agent loglarini ko'rish** (`Agent Logs`)
- Barcha agent faoliyati
- Xatolar va ogohlantirishlar
- Tizim holati

---

### 2. Dashboard (Asosiy Sahifa)

**Manzil**: http://127.0.0.1:8080/

Dashboard orqali:
- ✅ Yangi diagnostika boshlash
- ✅ Statistikani ko'rish
- ✅ Agent holatlarini kuzatish
- ✅ So'nggi sessiyalarni ko'rish

---

## 🔬 Diagnostika Qilish (Asosiy Funksiya)

### Qadamma-Qadam Yo'riqnoma

#### 1-Qadam: Bemor Yaratish

Agar bemor yo'q bo'lsa, avval admin panelda bemor yarating:

1. http://127.0.0.1:8080/admin/ ga kiring
2. **Patients** → **Add Patient** tugmasini bosing
3. Quyidagi ma'lumotlarni kiriting:
   - **Ism** (First name)
   - **Familiya** (Last name)
   - **Tug'ilgan sana** (Date of birth)
   - **Jins** (Gender): Erkak/Ayol
   - **Telefon** (Phone)
   - **Email** (ixtiyoriy)
   - **Manzil** (Address)
   - **Qon guruhi** (Blood type)
   - **Allergiyalar** (Allergies): JSON format, masalan: `["Penitsil", "Yong'oq"]`
   - **Surunkali kasalliklar** (Chronic diseases): JSON format, masalan: `["Astma"]`
   - **Favqulodda aloqa** (Emergency contact)
4. **Save** tugmasini bosing

#### 2-Qadam: Diagnostika Boshlash

1. http://127.0.0.1:8080/ ga o'ting
2. **"Yangi Diagnostika Boshlash"** formasini to'ldiring:
   - **Bemorni tanlang**: Dropdown dan bemorni tanlang
   - **Simptomlar**: Vergul bilan ajratilgan holda kiriting
     - Masalan: `isitma, bosh og'rig'i, yo'tal, mushak og'rig'i`
   - **Harorat** (ixtiyoriy): Agar o'lchangan bo'lsa kiriting
     - Masalan: `38.5`
3. **"Diagnostika Boshlash"** tugmasini bosing

#### 3-Qadam: Natijalarni Ko'rish

Diagnostika tugagach, avtomatik ravishda natijalar sahifasiga o'tasiz yoki:
- Dashboard da **"So'nggi Diagnostika Sessiyalari"** jadvalidan sessiyani tanlang
- **"Ko'rish"** tugmasini bosing

Natijalar sahifasida ko'rasiz:
- ✅ Bemor ma'lumotlari
- ✅ Kiritilgan simptomlar
- ✅ Topilgan kasalliklar (ishonch darajasi bilan)
- ✅ Davolash rejalari
- ✅ Tavsiya etiladigan tahlillar

---

## 🤖 Agentlar Tizimi

Tizimda 5 ta maxsus agent ishlaydi:

### 1. **Symptom Agent** (Simptom Agenti)
- Bemorning simptomlarini tahlil qiladi
- Simptomlarni kategoriyalarga ajratadi
- Og'irlik darajasini baholaydi

### 2. **Analysis Agent** (Tahlil Agenti)
- Tibbiy tahlillarni baholaydi
- Test natijalarini tahlil qiladi
- Qo'shimcha tahlillar tavsiya qiladi

### 3. **Diagnosis Agent** (Diagnoz Agenti)
- Kasalliklarni aniqlaydi
- Ishonch darajasini hisoblab chiqadi
- Eng mos keladigan kasalliklarni tanlaydi

### 4. **Treatment Agent** (Davolash Agenti)
- Davolash rejasini tuzadi
- Dori-darmonlarni tavsiya qiladi
- Hayot tarzi bo'yicha maslahatlar beradi

### 5. **Coordinator Agent** (Koordinator Agent)
- Barcha agentlarni boshqaradi
- Jarayonni muvofiqlashtiradi
- Natijalarni yig'adi va saqlaydi

---

## 📊 Statistika va Monitoring

### Dashboard Statistikasi

Dashboard da quyidagi statistikalarni ko'rasiz:

- **Jami Bemorlar**: Tizimda ro'yxatdan o'tgan bemorlar soni
- **Jami Sessiyalar**: Barcha diagnostika sessiyalari
- **Yakunlangan**: Muvaffaqiyatli yakunlangan diagnostikalar
- **Jarayonda**: Hozir bajarilayotgan diagnostikalar

### Agent Holatlari

Har bir agentning hozirgi holatini ko'rish mumkin:
- 🟢 **IDLE**: Kutish holatida
- 🟡 **PROCESSING**: Ishlamoqda
- 🔵 **COMPLETED**: Yakunlandi
- 🔴 **FAILED**: Xatolik yuz berdi

---

## 🔧 Muammolarni Hal Qilish

### Server Ishlamayapti?

```bash
# Virtual environment aktivlashtirilganligini tekshiring
python --version  # 3.10.1 bo'lishi kerak

# Serverni qayta ishga tushiring
python manage.py runserver 8080
```

### Static Fayllar Ko'rinmayapti?

```bash
python manage.py collectstatic --noinput
```

### Ma'lumotlar Bazasi Xatosi?

```bash
# Migratsiyalarni qayta ishga tushiring
python manage.py migrate
```

### Admin Parolini Unutdingizmi?

```bash
python set_admin_password.py
```

---

## 📝 Test Ma'lumotlar

### Test Bemor Yaratish

```bash
python create_test_patient.py
```

Bu script quyidagi test bemorni yaratadi:
- **Ism**: Alisher Karimov
- **Yosh**: 35 yosh
- **Jins**: Erkak
- **Telefon**: +998901234567

### Diagnostika Jarayonini Test Qilish

```bash
python test_diagnostic_flow.py
```

Bu script:
1. Test bemorni oladi
2. Test simptomlarni kiritadi
3. Diagnostika jarayonini boshlaydi
4. Natijalarni ko'rsatadi

---

## 🌐 API Dokumentatsiya

**Faqat admin foydalanuvchilar uchun!**

API dokumentatsiyasini ko'rish uchun:
1. Admin sifatida tizimga kiring
2. http://127.0.0.1:8080/api/docs/ ga o'ting

API Endpoints:
- `/api/v1/patients/` - Bemorlar
- `/api/v1/diagnostics/sessions/` - Diagnostika sessiyalari
- `/api/v1/diagnostics/results/` - Natijalar
- `/api/v1/agents/` - Agentlar

---

## 📚 Qo'shimcha Ma'lumotlar

### Kasalliklar Bazasi

Tizimda 5 ta kasallik mavjud:
1. **Gripp** - Gripp virusi infeksiyasi
2. **Shamollash (ORVI)** - Yuqori nafas yollari virusli infeksiyasi
3. **Bronxit** - Bronxlar yalliglanishi
4. **Gastrit** - Oshqozon shilliq qavatining yalliglanishi
5. **Migren** - Kuchli bosh og'rig'i

Yangi kasalliklar admin panelda qo'shilishi mumkin.

### Simptomlar Ro'yxati

Tizim quyidagi simptomlarni taniydi:
- Isitma
- Bosh og'rig'i
- Yo'tal
- Mushak og'rig'i
- Tomoq og'rig'i
- Burun bitishi
- Halsizlik
- Ko'ngil aynishi
- Qorin og'rig'i
- Va boshqalar...

---

## 🎯 Keyingi Qadamlar

1. ✅ Tizimni ishga tushiring
2. ✅ Admin panelga kiring
3. ✅ Test bemor yarating
4. ✅ Diagnostika qiling
5. ✅ Natijalarni ko'ring

---

## 📞 Yordam

Agar savollar bo'lsa:
- Admin panel: http://127.0.0.1:8080/admin/
- Dashboard: http://127.0.0.1:8080/
- Loglar: `logs/medical_mas.log`

---

**Omad tilaymiz! 🚀**
