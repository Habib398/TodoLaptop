"""
CONFIGURACIÓN ASGI PARA EL PROYECTO TODOLAP
============================================

ASGI (Asynchronous Server Gateway Interface) es el estándar de Python para
aplicaciones web asíncronas y protocolos que requieren conexiones de larga duración.

Este archivo expone la aplicación ASGI como una variable de módulo llamada ``application``.

¿CUÁNDO USAR ASGI EN LUGAR DE WSGI?
    - WebSockets (chat en tiempo real, notificaciones push)
    - Server-Sent Events (SSE)
    - HTTP/2
    - Long polling
    - Aplicaciones que necesitan manejar muchas conexiones simultáneas

SERVIDORES ASGI COMUNES:
    - Uvicorn (recomendado, basado en uvloop)
    - Daphne (desarrollado por Django Channels)
    - Hypercorn

USO EN DESARROLLO:
    python manage.py runserver  (Django 3.0+ usa ASGI por defecto)

USO EN PRODUCCIÓN:
    uvicorn TodoLap.asgi:application --host 0.0.0.0 --port 8000

NOTA IMPORTANTE:
    Para características asíncronas avanzadas (WebSockets, etc.), 
    instalar Django Channels:
        pip install channels
    
    Y agregar 'channels' a INSTALLED_APPS en settings.py

Para más información sobre este archivo, ver:
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Establecer el módulo de configuración por defecto de Django
# Apunta a TodoLap.settings (archivo settings.py en la carpeta TodoLap)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TodoLap.settings')

# Crear la aplicación ASGI
# Esta es la variable que los servidores ASGI buscan para servir la aplicación
application = get_asgi_application()
