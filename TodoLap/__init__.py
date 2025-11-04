"""
PAQUETE TODOLAP - CONFIGURACIÓN PRINCIPAL
==========================================

Este archivo marca el directorio TodoLap como un paquete de Python.

PROPÓSITO:
    - Permite que Python trate este directorio como un módulo importable
    - Contiene la configuración principal del proyecto Django (settings.py, urls.py)
    - Define el entry point para WSGI y ASGI

CONTENIDO DEL PAQUETE:
    - settings.py : Configuración principal del proyecto
    - urls.py     : Enrutamiento principal de URLs
    - wsgi.py     : Entry point para servidores WSGI
    - asgi.py     : Entry point para servidores ASGI

INICIALIZACIÓN:
    Este archivo normalmente está vacío, pero puede usarse para:
    - Configurar el logging del proyecto
    - Inicializar conexiones a servicios externos
    - Definir variables de módulo que necesitan estar disponibles al importar

NOTA:
    En versiones antiguas de Django (< 3.2), este archivo se usaba para
    configurar Celery o otros servicios. En versiones modernas, esto se
    hace en archivos separados o en settings.py.
"""

# Por el momento, este archivo está vacío intencionalmente
# Django solo requiere que exista para identificar este directorio como paquete Python