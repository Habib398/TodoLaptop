from django.apps import AppConfig


class ServiciosConfig(AppConfig):
    """
    Configuración de la aplicación Servicios.
    
    Esta clase define la configuración básica de la aplicación que maneja
    el catálogo de servicios, cotizaciones y ventas de servicios del sistema TodoLap.
    
    Características principales:
    - Gestión de tipos de servicios ofrecidos
    - Creación de cotizaciones para clientes
    - Seguimiento de servicios pagados
    - Integración con inventario para productos utilizados
    """
    
    # Tipo de campo automático por defecto para las claves primarias
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación (debe coincidir con el nombre del directorio)
    name = 'servicios'
