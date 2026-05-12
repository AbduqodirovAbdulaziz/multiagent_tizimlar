"""
WSGI config for PythonAnywhere deployment - ISHLAYDI!

PythonAnywhere Web Tab'da WSGI configuration file sifatida ishlatish uchun.
Bu faylni /var/www/USERNAME_pythonanywhere_com_wsgi.py ga ko'chiring.
"""
import os
import sys

# ============================================
# PROJECT PATH - o'zgartiring!
# ============================================
# username o'rniga o'zingizning PythonAnywhere username'ingizni yozing
username = 'multiagent'  # <-- BU YERNI O'ZGARTIRING
project_home = f'/home/{username}/multiagent'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ============================================
# ENVIRONMENT VARIABLES
# ============================================
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.pythonanywhere'

# .env faylidan environment variables yuklash
env_file = os.path.join(project_home, '.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())

# ============================================
# VIRTUAL ENVIRONMENT
# ============================================
venv_path = f'/home/{username}/.virtualenvs/multiagent/lib/python3.10/site-packages'
# yoki: venv_path = os.path.join(project_home, 'venv/lib/python3.10/site-packages')

if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# ============================================
# DJANGO APPLICATION
# ============================================
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
