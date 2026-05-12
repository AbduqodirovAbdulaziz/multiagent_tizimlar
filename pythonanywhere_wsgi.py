"""
WSGI config for PythonAnywhere deployment

Bu faylni PythonAnywhere Web Tab'da WSGI configuration file sifatida ishlatish kerak.

Path: /var/www/multiagent_pythonanywhere_com_wsgi.py
"""

import os
import sys

# ============================================
# PROJECT PATH
# ============================================
# O'zingizning username'ingizga qarab o'zgartiring
project_home = '/home/multiagent/multiagent_tizimlar'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ============================================
# ENVIRONMENT VARIABLES
# ============================================
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.dev'  # yoki 'config.settings.prod'

# ============================================
# VIRTUAL ENVIRONMENT
# ============================================
# Virtual environment'ni faollashtirish
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')

# Python 3.10+ uchun activate_this.py bo'lmasligi mumkin
# Shuning uchun site-packages'ni to'g'ridan-to'g'ri qo'shamiz
venv_site_packages = os.path.join(project_home, 'venv/lib/python3.10/site-packages')
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

# ============================================
# DJANGO APPLICATION
# ============================================
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
