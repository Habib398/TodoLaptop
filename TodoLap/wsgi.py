"""
CONFIGURACIÓN WSGI PARA EL PROYECTO TODOLAP
============================================

WSGI (Web Server Gateway Interface) es el estándar de Python para la comunicación
entre servidores web y aplicaciones web.

Este archivo expone la aplicación WSGI como una variable de módulo llamada ``application``.

USO EN DESARROLLO:
    python manage.py runserver

USO EN PRODUCCIÓN:
    - Gunicorn: gunicorn TodoLap.wsgi:application
    - uWSGI: uwsgi --http :8000 --wsgi-file TodoLap/wsgi.py
    - Apache + mod_wsgi: configurar en httpd.conf o .wsgi file

SERVIDORES WSGI COMUNES:
    - Gunicorn (recomendado para Django)
    - uWSGI
    - mod_wsgi (Apache)
    - Waitress (Windows)

CONFIGURACIÓN TÍPICA DE PRODUCCIÓN (Gunicorn):
    gunicorn --workers 3 --bind 0.0.0.0:8000 TodoLap.wsgi:application

Para más información sobre este archivo, ver:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Establecer el módulo de configuración por defecto de Django
# Apunta a TodoLap.settings (archivo settings.py en la carpeta TodoLap)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TodoLap.settings')

# Crear la aplicación WSGI
# Esta es la variable que los servidores WSGI buscan para servir la aplicación
application = get_wsgi_application()
