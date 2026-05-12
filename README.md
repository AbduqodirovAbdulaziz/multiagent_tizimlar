# Sog'liqni saqlashda Multiagent Tizimlar: Tibbiy Diagnostika Platformasi

## Loyiha haqida

Bu loyiha sog'liqni saqlash sohasida multiagent tizim (MAS) kontseptsiyasini Django framework orqali amalga oshiradi. Tizim FIPA-ACL kommunikatsiya protokoli asosida ishlaydi va 5 ta ixtisoslashtirilgan agent orqali tibbiy diagnostika jarayonini avtomatlashtiradi.

## Arxitektura

### Multiagent Tizim Komponentlari

1. **SimptomlarAgenti** - Bemor simptomlarini tahlil qiladi
2. **TahlilAgenti** - Tibbiy tahlillarni baholaydi
3. **DiagnozAgenti** - Kasallik diagnozini aniqlaydi
4. **DavolanishAgenti** - Davolash rejasini taklif qiladi
5. **KoordinatorAgenti** - Barcha agentlarni muvofiqlashtiradi

### Texnologiyalar

- **Backend**: Python 3.10.1, Django 4.2.30 LTS, Django REST Framework
- **Database**: SQLite3 (development), PostgreSQL (production)
- **Frontend**: Django Templates + HTMX
- **Admin Panel**: Django Jazzmin
- **Testing**: pytest-django
- **Deployment**: PythonAnywhere (free tier compatible)

## Tezkor Ishga Tushirish

### 1. Muhit sozlash

```bash
# Virtual environment yaratish (Python 3.10.1)
python -m venv venv310
venv310\Scripts\activate  # Windows

# Bog'liqliklarni o'rnatish
pip install -r requirements/dev.txt
```

### 2. Django sozlash

```bash
# Migratsiyalar
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Static fayllarni yig'ish
python manage.py collectstatic --noinput

# Development server (port 8080)
python manage.py runserver 8080
```

### 3. Tizimdan foydalanish

1. **Admin Panel**: http://127.0.0.1:8080/admin/
   - Bemorlarni qo'shish va boshqarish
   - Kasallik naqshlarini boshqarish
   - Tizim sozlamalari

2. **Dashboard**: http://127.0.0.1:8080/
   - Yangi diagnostika boshlash
   - Sessiyalar va natijalarni ko'rish
   - Agent holatlari monitoring

3. **API Docs**: http://127.0.0.1:8080/api/docs/ (faqat admin uchun)
   - API dokumentatsiyasi
   - Swagger UI

## API Endpoints

### Diagnostika API
- `POST /api/diagnostics/sessions/` - Yangi diagnostika sessiyasi yaratish
- `GET /api/diagnostics/sessions/` - Barcha sessiyalarni ko'rish
- `GET /api/diagnostics/sessions/{id}/` - Sessiya detallari
- `GET /api/diagnostics/results/` - Diagnostika natijalari

### Bemorlar API
- `GET /api/patients/` - Bemorlar ro'yxati
- `GET /api/patients/{id}/` - Bemor detallari
- `GET /api/patients/{id}/sessions/` - Bemor sessiyalari

### Agentlar API
- `GET /api/agents/states/` - Barcha agentlar holati
- `POST /api/agents/coordinate/` - Koordinator agentni ishga tushirish

**Eslatma:** API dokumentatsiya faqat admin foydalanuvchilar uchun ochiq.

## Testing

```bash
# Barcha testlarni ishga tushirish
pytest

# Coverage bilan
pytest --cov=. --cov-report=html

# Muayyan app testlari
pytest apps/agents/tests/

# Django shell orqali test
python manage.py shell
```

## Diagnostika Jarayoni

### 1. Bemor Qo'shish
Admin panelda yangi bemor qo'shing:
- Shaxsiy ma'lumotlar (ism, familiya, tug'ilgan sana)
- Tibbiy ma'lumotlar (qon guruhi, allergiyalar, surunkali kasalliklar)
- Aloqa ma'lumotlari

### 2. Diagnostika Boshlash
Dashboard'da diagnostika formasini to'ldiring:
- Bemorni tanlang
- Simptomlarni checkbox orqali belgilang (40+ simptom, 7 kategoriya)
- Haroratni kiriting (ixtiyoriy)
- "Diagnostika Boshlash" tugmasini bosing

### 3. Agent Jarayoni
Tizim avtomatik ravishda quyidagi agentlarni ishga tushiradi:
1. **SymptomAgent** - Simptomlarni tahlil qiladi va kategoriyalaydi
2. **AnalysisAgent** - Tibbiy tahlillarni baholaydi
3. **DiagnosisAgent** - Kasallik diagnozini aniqlaydi
4. **TreatmentAgent** - Davolash rejasini taklif qiladi
5. **CoordinatorAgent** - Barcha jarayonni muvofiqlashtiradi

### 4. Natijalarni Ko'rish
- Diagnostika yakunlangandan keyin natijalar sahifasiga yo'naltirilasiz
- Har bir diagnoz uchun ishonch darajasi ko'rsatiladi
- Tavsiya etilgan davolash rejasi va tahlillar

## Xususiyatlar

### ✅ Amalga Oshirilgan
- 5 ta ixtisoslashtirilgan agent
- FIPA-ACL kommunikatsiya protokoli
- BDI (Belief-Desire-Intention) arxitektura
- 40+ simptom, 7 kategoriya
- Kasallik naqshlari bazasi (5 ta kasallik)
- Admin panel (Django Jazzmin)
- Dashboard monitoring
- RESTful API
- Diagnostika sessiyalari
- Natijalar tahlili

### 🔄 Kelajakda Qo'shilishi Mumkin
- Real-time agent monitoring (WebSocket)
- Tibbiy tahlillar integratsiyasi
- Machine Learning modellari
- Bemor tarixi tahlili
- PDF export funksiyasi
- Email bildirishnomalar
- Multi-language support

## Loyiha Strukturasi

```
medical_mas/
├── apps/
│   ├── core/           # Bazaviy Agent sinfi, ACL xabarlar
│   ├── agents/         # 5 ta agent implementatsiyasi
│   ├── patients/       # Bemor modellari
│   ├── diagnostics/    # Diagnostika sessiyalari
│   ├── dashboard/      # Monitoring va vizualizatsiya
│   └── api/            # DRF API
├── config/             # Django sozlamalari
├── requirements/       # Bog'liqliklar
├── docker/             # Docker konfiguratsiyalari
└── tests/              # Testlar
```

## Akademik Jihat

Bu loyiha quyidagi multiagent tizim kontseptsiyalarini amalga oshiradi:

- **FIPA-ACL Protokoli**: Agentlar o'rtasida standartlashtirilgan xabar almashish
- **BDI Arxitektura**: Belief-Desire-Intention agent modeli
- **Koordinatsiya Mexanizmi**: Markaziy koordinator orqali vazifalarni taqsimlash
- **Parallel Bajarish**: Celery orqali agentlarni parallel ishlatish
- **Xabar Navbatlari**: Redis Pub/Sub orqali asinxron kommunikatsiya

## Litsenziya

MIT License - Akademik maqsadlar uchun
