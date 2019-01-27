"""
WSGI config for precisionFramework project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'precisionFramework.settings.production'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "precisionFramework.settings.production")

application = get_wsgi_application()