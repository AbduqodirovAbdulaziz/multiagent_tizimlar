# Loyiha Strukturasi

```
medical_mas/
│
├── apps/                           # Django applications
│   ├── __init__.py
│   │
│   ├── core/                       # Bazaviy agent sinfi va umumiy utilities
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # ACLMessage, BaseAgent
│   │   ├── constants.py           # FIPA-ACL konstantalar
│   │   ├── exceptions.py          # Custom exceptions
│   │   ├── utils.py               # Helper functions
│   │   ├── urls.py                # Health check endpoint
│   │   └── views.py               # Health check view
│   │
│   ├── agents/                     # 5 ta agent implementatsiyasi
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # Agent holati modellari
│   │   ├── base.py                # Agent bazaviy sinfi
│   │   ├── symptom_agent.py      # SimptomlarAgenti
│   │   ├── analysis_agent.py     # TahlilAgenti
│   │   ├── diagnosis_agent.py    # DiagnozAgenti
│   │   ├── treatment_agent.py    # DavolanishAgenti
│   │   ├── coordinator_agent.py  # KoordinatorAgenti
│   │   ├── tasks.py               # Celery tasks
│   │   ├── services.py            # Business logic
│   │   └── admin.py               # Admin interface
│   │
│   ├── patients/                   # Bemor ma'lumotlari
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # Patient, Symptom, MedicalHistory
│   │   ├── admin.py
│   │   └── managers.py            # Custom model managers
│   │
│   ├── diagnostics/                # Diagnostika sessiyalari
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py              # DiagnosticSession, DiseasePattern, Result
│   │   ├── services.py            # Diagnostika business logic
│   │   ├── admin.py
│   │   └── signals.py             # Django signals
│   │
│   ├── dashboard/                  # Monitoring va vizualizatsiya
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── views.py               # Dashboard views
│   │   ├── urls.py
│   │   └── templates/
│   │       └── dashboard/
│   │           ├── index.html
│   │           ├── agent_status.html
│   │           └── session_detail.html
│   │
│   └── api/                        # DRF API
│       ├── __init__.py
│       ├── apps.py
│       ├── urls.py                # API routing
│       ├── serializers.py         # DRF serializers
│       ├── views.py               # API ViewSets
│       ├── permissions.py         # Custom permissions
│       ├── exceptions.py          # API exception handler
│       └── pagination.py          # Custom pagination
│
├── config/                         # Django settings
│   ├── __init__.py
│   ├── celery.py                  # Celery configuration
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py                    # Root URL configuration
│   └── settings/
│       ├── __init__.py
│       ├── base.py                # Base settings
│       ├── dev.py                 # Development settings
│       ├── prod.py                # Production settings
│       └── test.py                # Test settings
│
├── docker/                         # Docker konfiguratsiyalari
│   ├── Dockerfile
│   └── nginx/
│       └── nginx.conf
│
├── requirements/                   # Python dependencies
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── static/                         # Static files (CSS, JS, images)
│   └── .gitkeep
│
├── media/                          # User uploaded files
│   └── .gitkeep
│
├── templates/                      # Django templates
│   └── base.html
│
├── logs/                           # Application logs
│   └── .gitkeep
│
├── tests/                          # Integration tests
│   └── __init__.py
│
├── fixtures/                       # Test data
│   └── diseases.json
│
├── .env.example                    # Environment variables template
├── .gitignore
├── docker-compose.yml
├── manage.py
├── Makefile
├── pytest.ini
├── setup.cfg
├── README.md
└── PROJECT_STRUCTURE.md
```

## Arxitektura Tushuntirishlari

### 1. Apps Tuzilmasi

**core/** - Barcha agentlar uchun umumiy bazaviy sinf va utilities:
- `BaseAgent` - Abstrakt agent sinfi (BDI arxitektura)
- `ACLMessage` - FIPA-ACL xabar modeli
- Custom exceptions va utility functions

**agents/** - 5 ta ixtisoslashtirilgan agent:
- Har bir agent alohida Python sinfi
- Celery tasks orqali parallel bajarish
- Redis Pub/Sub orqali kommunikatsiya

**patients/** - Bemor ma'lumotlari:
- Patient profili
- Simptomlar tarixi
- Tibbiy tarix

**diagnostics/** - Diagnostika jarayoni:
- DiagnosticSession - har bir diagnostika sessiyasi
- DiseasePattern - kasallik naqshlari bazasi
- Result - yakuniy natijalar

**dashboard/** - Real-vaqt monitoring:
- Agent holati ko'rish
- Diagnostika jarayonini kuzatish
- HTMX orqali real-vaqt yangilanishlar

**api/** - RESTful API:
- DRF ViewSets va Serializers
- API versiyalash (v1)
- JWT authentication

### 2. Multiagent Tizim Kontseptsiyalari

**FIPA-ACL Protokoli:**
- Standartlashtirilgan xabar formati
- Performatives: INFORM, REQUEST, QUERY, PROPOSE, etc.
- ACLMessage modelida saqlanadi

**BDI Arxitektura:**
- Belief (e'tiqod) - agent bilimi
- Desire (istak) - maqsadlar
- Intention (niyat) - rejalar

**Koordinatsiya:**
- KoordinatorAgent markaziy boshqaruvchi
- Pipeline pattern - ketma-ket agent chaqirish
- Error handling va retry mexanizmi

**Parallel Bajarish:**
- Celery worker'lar orqali
- Redis message queue
- Asinxron task execution

### 3. Texnologik Tanlovlar

**PostgreSQL:**
- Relational data uchun
- ACID xususiyatlari
- Complex queries

**Redis:**
- Agent xabar navbatlari
- Cache
- Pub/Sub messaging

**Celery:**
- Asinxron task execution
- Distributed task queue
- Retry va error handling

**HTMX:**
- Real-vaqt UI yangilanishlar
- Minimal JavaScript
- Server-side rendering

## Keyingi Bosqichlar

1. ✅ BOSQICH 1 - Loyiha tuzilmasi va sozlash
2. ⏳ BOSQICH 2 - Core modellar va agent bazasi
3. ⏳ BOSQICH 3 - Agent implementatsiyasi
4. ⏳ BOSQICH 4 - DRF API va serializers
5. ⏳ BOSQICH 5 - Dashboard va frontend
6. ⏳ BOSQICH 6 - Test va deployment
