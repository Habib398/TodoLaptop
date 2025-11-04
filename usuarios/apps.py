from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """
    Configuración de la aplicación Usuarios.
    
    Esta clase define la configuración básica de la aplicación que maneja
    la autenticación, autorización y gestión de usuarios del sistema TodoLap.
    
    CARACTERÍSTICAS PRINCIPALES:
    - Sistema de autenticación personalizado con modelo Usuario extendido
    - Gestión de roles (admin, técnico)
    - Control de acceso basado en roles
    - CRUD completo de usuarios (solo para administradores)
    - Dashboard personalizado según permisos
    
    MODELO PERSONALIZADO:
    El sistema usa usuarios.Usuario en lugar del modelo User por defecto.
    Configurado en settings.py: AUTH_USER_MODEL = 'usuarios.Usuario'
    
    PERMISOS POR ROL:
    - Admin: Acceso completo + gestión de usuarios
    - Técnico: Acceso a inventario, servicios y ventas
    """
    
    # Tipo de campo automático por defecto para las claves primarias
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación (debe coincidir con el nombre del directorio)
    name = 'usuarios'
