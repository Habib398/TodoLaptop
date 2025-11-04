from django.contrib.auth.models import AbstractUser
from django.db import models

# ==================== MODELO PERSONALIZADO DE USUARIO ====================

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser de Django.
    
    Extiende el modelo de usuario por defecto de Django para agregar campos
    y funcionalidades específicas del sistema TodoLap.
    
    CAMPOS ADICIONALES:
    - rol: Define el tipo de usuario y sus permisos en el sistema
    
    CAMPOS HEREDADOS DE AbstractUser:
    - username: Nombre de usuario único
    - password: Contraseña hasheada
    - first_name: Nombre
    - last_name: Apellido
    - email: Correo electrónico
    - is_staff: Puede acceder al admin de Django
    - is_active: Usuario activo/inactivo
    - is_superuser: Superusuario con todos los permisos
    - date_joined: Fecha de registro
    - last_login: Último inicio de sesión
    
    ROLES DEL SISTEMA:
    - admin: Administrador con acceso completo
        * Gestión de usuarios (crear, editar, eliminar)
        * Acceso a todos los módulos
        * Configuración del sistema
    
    - tecnico: Usuario técnico con permisos limitados
        * Acceso a inventario, servicios y ventas
        * No puede gestionar usuarios
        * Puede realizar cotizaciones y ventas
    
    USO:
        # Crear usuario
        usuario = Usuario.objects.create_user(
            username='juan',
            password='password123',
            rol='tecnico'
        )
        
        # Verificar rol
        if usuario.rol == 'admin':
            # Permitir acceso a gestión de usuarios
            pass
    """
    
    # Definición de roles disponibles en el sistema
    # Tuplas en formato (valor_bd, etiqueta_legible)
    ROLES = (
        ('admin', 'Administrador'),    # Acceso completo al sistema
        ('tecnico', 'Técnico'),        # Acceso limitado a operaciones
    )
    
    # Campo de rol con opciones predefinidas
    # max_length=20: Longitud máxima del campo
    # choices=ROLES: Limita valores a los definidos en ROLES
    # default='tecnico': Valor por defecto al crear usuarios
    rol = models.CharField(max_length=20, choices=ROLES, default='tecnico')

    def __str__(self):
        """
        Representación en string del usuario.
        
        Formato: "username (rol)"
        Ejemplo: "juan.perez (Técnico)"
        
        Returns:
            str: Username y rol del usuario
        """
        return f"{self.username} ({self.rol})"
