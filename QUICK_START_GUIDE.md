# Medical Multiagent System - Quick Start Guide

## 🚀 Getting Started

### 1. Activate Virtual Environment

```bash
# Windows
venv310\Scripts\activate

# Linux/Mac
source venv310/bin/activate
```

### 2. Run Development Server

```bash
python manage.py runserver 8080
```

Server will start at: **http://127.0.0.1:8080/**

---

## 🔐 Admin Access

### Admin Panel
- **URL:** http://127.0.0.1:8080/admin/
- **Username:** admin
- **Password:** admin123

### Features
- Patient management
- Disease pattern management
- Diagnostic session monitoring
- Agent status tracking
- System logs

---

## 📊 Dashboard

### Main Dashboard
- **URL:** http://127.0.0.1:8080/
- View statistics
- Recent sessions
- Agent status

### Session Details
- **URL:** http://127.0.0.1:8080/session/{session_id}/
- View diagnostic results
- See agent states
- Check recommendations

---

## 🔌 API Endpoints

### Base URL
```
http://127.0.0.1:8080/api/v1/
```

### API Documentation
- **Swagger UI:** http://127.0.0.1:8080/api/docs/
- **ReDoc:** http://127.0.0.1:8080/api/redoc/
- **Schema:** http://127.0.0.1:8080/api/schema/

### Key Endpoints

#### Create Diagnostic Session
```bash
POST /api/v1/diagnostics/
Content-Type: application/json
Authorization: Token YOUR_TOKEN

{
  "patient_id": 1,
  "symptoms": ["isitma", "bosh og'rig'i", "yo'tal"],
  "test_results": {"temperature": 38.5}
}
```

#### Get Session Status
```bash
GET /api/v1/diagnostics/{id}/status/
```

#### Get Session Results
```bash
GET /api/v1/diagnostics/{id}/results/
```

#### List Patients
```bash
GET /api/v1/patients/
```

#### Agent Health Check
```bash
GET /api/v1/agents/health/
```

---

## 🧪 Testing

### Run System Check
```bash
python manage.py check
```

### Run Diagnostic Flow Test
```bash
python test_diagnostic_flow.py
```

### Run Django Tests
```bash
python manage.py test
```

---

## 📝 Common Tasks

### Create Superuser
```bash
python manage.py createsuperuser
```

### Load Sample Data
```bash
python manage.py load_sample_data
```

### Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### View Logs
```bash
# Check log file
cat logs/medical_mas.log

# Or view in admin panel
# Admin > Agent Logs
```

---

## 🤖 Agent System

### Available Agents

1. **SymptomAgent** - Analyzes symptoms
2. **AnalysisAgent** - Evaluates test results
3. **DiagnosisAgent** - Makes diagnoses
4. **TreatmentAgent** - Creates treatment plans
5. **CoordinatorAgent** - Orchestrates all agents

### Agent States
- `IDLE` - Waiting for tasks
- `PROCESSING` - Currently working
- `COMPLETED` - Task finished
- `FAILED` - Error occurred

### Monitor Agents
- **Dashboard:** http://127.0.0.1:8080/agents/
- **API:** http://127.0.0.1:8080/api/v1/agents/
- **Admin:** Admin > Agent States

---

## 🏥 Using the System

### Step 1: Create Patient
1. Go to Admin Panel
2. Click "Patients" → "Add Patient"
3. Fill in patient information
4. Save

### Step 2: Add Disease Patterns (if needed)
1. Go to Admin Panel
2. Click "Disease Patterns" → "Add Disease Pattern"
3. Fill in disease information
4. Add symptoms (comma-separated)
5. Save

### Step 3: Create Diagnostic Session

**Option A: Via API**
```python
import requests

response = requests.post(
    'http://127.0.0.1:8080/api/v1/diagnostics/',
    json={
        'patient_id': 1,
        'symptoms': ['isitma', 'bosh og\'rig\'i', 'yo\'tal'],
        'test_results': {'temperature': 38.5}
    },
    headers={'Authorization': 'Token YOUR_TOKEN'}
)

print(response.json())
```

**Option B: Via Python Script**
```python
from apps.patients.models import Patient
from apps.diagnostics.services import DiagnosticService
from apps.agents.coordinator_agent import CoordinatorAgent

# Get patient
patient = Patient.objects.get(id=1)

# Create session
session = DiagnosticService.create_session(
    patient=patient,
    symptoms=['isitma', 'bosh og\'rig\'i', 'yo\'tal']
)

# Run diagnostic
coordinator = CoordinatorAgent()
result = coordinator.execute({
    'session_id': session.session_id,
    'patient_id': patient.id,
    'symptoms': ['isitma', 'bosh og\'rig\'i', 'yo\'tal'],
    'test_results': {'temperature': 38.5}
})

print(result)
```

### Step 4: View Results
1. Go to Dashboard
2. Click on session
3. View diagnostic results
4. Check treatment recommendations

---

## 🔧 Troubleshooting

### Server Won't Start
```bash
# Check if port is in use
netstat -ano | findstr :8080

# Use different port
python manage.py runserver 8000
```

### Database Errors
```bash
# Reset database (WARNING: deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements/dev.txt
```

### Agent Errors
```bash
# Check agent logs
python manage.py shell
>>> from apps.core.models import AgentLog
>>> logs = AgentLog.objects.filter(level='ERROR').order_by('-timestamp')[:10]
>>> for log in logs:
...     print(f"{log.agent_name}: {log.message}")
```

---

## 📚 Additional Resources

### Documentation Files
- `README.md` - Project overview
- `PROJECT_STRUCTURE.md` - Code organization
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `PYTHONANYWHERE_DEPLOYMENT.md` - PythonAnywhere specific guide
- `PROJECT_ANALYSIS_REPORT.md` - Complete analysis

### Configuration Files
- `.env` - Environment variables
- `config/settings/` - Django settings
- `requirements/` - Dependencies

### Key Directories
- `apps/` - Django applications
- `config/` - Project configuration
- `templates/` - HTML templates
- `static/` - Static files
- `media/` - User uploads
- `logs/` - Application logs

---

## 💡 Tips

1. **Always activate virtual environment** before running commands
2. **Check logs** if something doesn't work
3. **Use admin panel** for quick data management
4. **Test API** with Swagger UI before integration
5. **Monitor agents** to ensure they're working
6. **Backup database** before major changes

---

## 🆘 Getting Help

### Check Logs
```bash
# Application logs
tail -f logs/medical_mas.log

# Django logs
python manage.py runserver --verbosity 2
```

### Django Shell
```bash
python manage.py shell

# Test imports
>>> from apps.agents.coordinator_agent import CoordinatorAgent
>>> coordinator = CoordinatorAgent()
>>> print(coordinator.agent_name)
```

### System Check
```bash
python manage.py check --deploy
```

---

**Last Updated:** May 12, 2026  
**Version:** 1.0.0  
**Python:** 3.10.1  
**Django:** 4.2.30 LTS
