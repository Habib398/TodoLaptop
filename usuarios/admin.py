from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# ==================== REGISTRO DE MODELOS EN ADMIN ====================

# Registrar el modelo Usuario en el panel de administración de Django
# Usa UserAdmin para aprovechar la interfaz estándar de gestión de usuarios
# Esto permite gestionar usuarios desde /admin/usuarios/usuario/
admin.site.register(Usuario, UserAdmin)
