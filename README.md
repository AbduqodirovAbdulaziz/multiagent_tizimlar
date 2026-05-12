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

- **Backend**: Python 3.11+, Django 5.x, Django REST Framework
- **Database**: PostgreSQL (asosiy), Redis (xabar navbatlari)
- **Asinxron**: Celery + Redis
- **Frontend**: Django Templates + HTMX
- **Testing**: pytest-django, factory_boy
- **Deployment**: PythonAnywhere / Heroku / VPS

## Tezkor Ishga Tushirish

### 1. Muhit sozlash

```bash
# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bog'liqliklarni o'rnatish
pip install -r requirements/dev.txt
```

### 2. PostgreSQL va Redis o'rnatish

**PostgreSQL:**
```bash
# Windows: https://www.postgresql.org/download/windows/
# PostgreSQL o'rnatilgandan keyin database yarating:
psql -U postgres
CREATE DATABASE medical_mas_db;
CREATE USER medical_mas_user WITH PASSWORD 'medical_mas_2024_secure';
GRANT ALL PRIVILEGES ON DATABASE medical_mas_db TO medical_mas_user;
\q
```

**Redis:**
```bash
# Windows: https://github.com/microsoftarchive/redis/releases
# Redis o'rnatib, redis-server ni ishga tushiring
redis-server
```

### 3. Django sozlash

```bash
# Migratsiyalar
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Static fayllarni yig'ish
python manage.py collectstatic --noinput

# Development server
python manage.py runserver
```

### 4. Celery ishga tushirish (ixtiyoriy - agent vazifalar uchun)

```bash
# Celery worker (alohida terminal)
celery -A config worker -l info

# Celery beat (alohida terminal)
celery -A config beat -l info
```

## API Endpoints

- `POST /api/v1/diagnostics/start/` - Yangi diagnostika sessiyasi
- `GET /api/v1/diagnostics/{id}/status/` - Agent holati
- `GET /api/v1/diagnostics/{id}/result/` - Yakuniy natija
- `GET /api/v1/agents/health/` - Barcha agentlar holati

## Testing

```bash
# Barcha testlarni ishga tushirish
pytest

# Coverage bilan
pytest --cov=. --cov-report=html

# Muayyan app testlari
pytest apps/agents/tests/
```

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
