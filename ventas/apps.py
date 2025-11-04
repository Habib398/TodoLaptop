"""
Configuración de la aplicación Ventas.

Este módulo define la configuración para el módulo de ventas del sistema
TodoLap, que gestiona el punto de venta y cobro de servicios.
"""

from django.apps import AppConfig


class VentasConfig(AppConfig):
    """
    Clase de configuración para el módulo de ventas.
    
    FUNCIONALIDADES DEL MÓDULO:
    - Punto de venta (POS) para productos del inventario
    - Cobro de servicios de reparación completados
    - Registro de ventas con detalles
    - Control de stock al vender productos
    - Historial de ventas y servicios pagados
    
    CARACTERÍSTICAS:
    - Sistema de carrito de compras en tiempo real
    - Búsqueda de productos para agregar a ventas
    - Gestión de servicios cotizados vs pagados
    - Transacciones atómicas para integridad de datos
    
    MODELOS REGISTRADOS:
    - Venta: Encabezado de venta
    - DetalleVenta: Líneas de productos vendidos
    """
    # Tipo de campo para primary keys (BigInt)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre del módulo
    name = 'ventas'
