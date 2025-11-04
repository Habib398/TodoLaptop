"""
Configuración de URLs del módulo de ventas.

Define las rutas para todas las vistas del módulo de ventas,
incluyendo punto de venta de productos y cobro de servicios.

RUTAS DISPONIBLES:
- '' (ventas): Página principal del módulo con opciones
- cobrar-productos/: Punto de venta (POS) para productos
- cobrar-servicios/: Gestión y cobro de servicios
- pagar-servicio/<id>/: Procesar pago de un servicio específico
- buscar-producto/: API AJAX para búsqueda de productos
"""

from django.urls import path
from .views import ventas_view, cobrar_productos, cobrar_servicios, buscar_producto, pagar_servicio

urlpatterns = [
    # Página principal de ventas (selector de opciones)
    path('', ventas_view, name='ventas'),
    
    # Punto de venta para productos del inventario
    path('cobrar-productos/', cobrar_productos, name='ventas_cobrar_productos'),
    
    # Gestión y cobro de servicios de reparación
    path('cobrar-servicios/', cobrar_servicios, name='ventas_cobrar_servicios'),
    
    # Procesar el pago de un servicio cotizado
    path('pagar-servicio/<int:servicio_id>/', pagar_servicio, name='pagar_servicio'),
    
    # API AJAX para búsqueda de productos (retorna JSON)
    path('buscar-producto/', buscar_producto, name='buscar_producto'),
]
