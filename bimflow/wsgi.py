"""
WSGI config for bimflow project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bimflow.settings')

application = get_wsgi_application()