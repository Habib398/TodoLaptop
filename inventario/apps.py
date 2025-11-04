from django.apps import AppConfig


class InventarioConfig(AppConfig):
    """
    Configuración de la aplicación Inventario.
    
    Esta clase define la configuración básica de la aplicación que maneja
    el inventario de productos del sistema TodoLap.
    """
    
    # Tipo de campo automático por defecto para las claves primarias
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación (debe coincidir con el nombre del directorio)
    name = 'inventario'
