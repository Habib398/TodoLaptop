"""
Configuración del administrador de Django para el módulo de ventas.

Este módulo registra los modelos de ventas en el panel de administración
de Django para permitir su gestión.

MODELOS DISPONIBLES:
- Venta: Encabezados de ventas realizadas
- DetalleVenta: Detalles de productos vendidos en cada venta

NOTA: Actualmente los modelos no están registrados en el admin.
Para registrarlos, descomentar y agregar:
    from .models import Venta, DetalleVenta
    admin.site.register(Venta)
    admin.site.register(DetalleVenta)
"""

from django.contrib import admin

# Register your models here.
# Los modelos de Venta y DetalleVenta pueden registrarse aquí
# para gestión desde el panel de administración de Django
