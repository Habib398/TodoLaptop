from django.contrib import admin
from .models import Producto

# ==================== REGISTRO DE MODELOS EN ADMIN ====================

# Registrar el modelo Producto en el panel de administración de Django
# Esto permite gestionar productos desde /admin/
admin.site.register(Producto)
