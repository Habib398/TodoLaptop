"""
CONFIGURACIÓN DE URLs PRINCIPAL - PROYECTO TODOLAP
==================================================

Este archivo define el enrutamiento principal del proyecto Django TodoLap.
Centraliza todas las URLs de las diferentes aplicaciones y funcionalidades.

ESTRUCTURA DE URLs:
- /admin/              : Panel de administración de Django
- /                    : Redirección automática al login
- /login/              : Página de inicio de sesión
- /logout/             : Cerrar sesión
- /dashboard/          : Panel principal tras login
- /usuarios/*          : Gestión de usuarios (solo admin)
- /inventario/*        : CRUD de productos
- /servicios/*         : CRUD de servicios y cotizaciones
- /ventas/*            : Módulo de ventas (incluido desde ventas.urls)

PERMISOS:
- Rutas públicas: login
- Rutas protegidas: todas las demás requieren @login_required
- Rutas de admin: solo para is_staff o is_superuser

ARCHIVOS ESTÁTICOS:
En modo DEBUG, Django sirve automáticamente archivos estáticos.
En producción, usar un servidor web (nginx, Apache) para servir estáticos.
"""

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importar vistas de inventario
from inventario import views

# Importar vistas de usuarios
from usuarios.views import (
    dashboard,           # Panel principal
    login_view,          # Inicio de sesión
    logout_view,         # Cerrar sesión
    agregar_usuario,     # Crear nuevo usuario
    listar_usuarios,     # Listado de usuarios
    editar_usuario,      # Editar usuario existente
    cambiar_estado_usuario,  # Activar/desactivar usuario
    eliminar_usuario     # Eliminar usuario
)

# Importar vistas de servicios
from servicios.views import (
    servicios_view,          # Vista principal de servicios
    agregar_servicio,        # Crear servicio
    modificar_servicio,      # Editar servicio
    eliminar_servicio,       # Eliminar servicio
    cotizar_servicio,        # Generar cotización
    obtener_producto_info    # Vista AJAX para info de productos
)

# ==================== DEFINICIÓN DE URLs ====================

urlpatterns = [
    # ========== PANEL DE ADMINISTRACIÓN ==========
    # Panel admin de Django (/admin/)
    # Requiere usuario con is_staff=True
    path("admin/", admin.site.urls),

    # ========== AUTENTICACIÓN ==========
    # Sistema de login/logout y dashboard principal
    path("login/", login_view, name="login"),           # Página de inicio de sesión
    path("logout/", logout_view, name="logout"),        # Cerrar sesión y redirigir a login
    path("dashboard/", dashboard, name="dashboard"),    # Panel principal tras autenticación
    
    # ========== GESTIÓN DE USUARIOS (Solo Admin) ==========
    # CRUD completo de usuarios, restringido a administradores
    path("usuarios/agregar/", agregar_usuario, name="agregar_usuario"),              # Crear usuario
    path("usuarios/listar/", listar_usuarios, name="listar_usuarios"),              # Listar usuarios
    path("usuarios/editar/<int:pk>/", editar_usuario, name="editar_usuario"),       # Editar usuario
    path("usuarios/estado/<int:pk>/", cambiar_estado_usuario, name="cambiar_estado_usuario"),  # Activar/desactivar
    path("usuarios/eliminar/<int:pk>/", eliminar_usuario, name="eliminar_usuario"), # Eliminar usuario

    # ========== REDIRECCIÓN RAÍZ ==========
    # Cuando se accede a la raíz (/), redirigir automáticamente al login
    # Usa lambda para evitar crear una vista separada
    path("", lambda request: redirect("login")),

    # ========== INVENTARIO - CRUD DE PRODUCTOS ==========
    # Gestión completa de productos del inventario
    path("inventario/", views.inventario_view, name="inventario"),                          # Listar productos
    path("inventario/agregar/", views.agregar_producto, name="agregar_producto"),          # Agregar producto
    path("inventario/modificar/<int:pk>/", views.modificar_producto, name="modificar_producto"),  # Modificar producto
    path("inventario/eliminar/<int:pk>/", views.eliminar_producto, name="eliminar_producto"),    # Eliminar producto
    
    # ========== SERVICIOS - GESTIÓN Y COTIZACIONES ==========
    # CRUD de servicios + sistema de cotización
    path("servicios/", servicios_view, name="servicios"),                                   # Listar servicios
    path("servicios/agregar/", agregar_servicio, name="agregar_servicio"),                 # Agregar servicio
    path("servicios/modificar/<int:pk>/", modificar_servicio, name="modificar_servicio"),  # Modificar servicio
    path("servicios/eliminar/<int:pk>/", eliminar_servicio, name="eliminar_servicio"),     # Eliminar servicio
    path("servicios/cotizar/<int:servicio_id>/", cotizar_servicio, name="cotizar_servicio"),  # Generar cotización
    path("servicios/producto-info/", obtener_producto_info, name="obtener_producto_info"), # AJAX: info de producto
    
    # ========== VENTAS - MÓDULO COMPLETO ==========
    # Incluye todas las URLs definidas en ventas/urls.py
    # Permite mantener las URLs de ventas organizadas en su propio archivo
    path("ventas/", include('ventas.urls')),
]

# ==================== SERVIR ARCHIVOS ESTÁTICOS EN DESARROLLO ====================

# Solo en modo DEBUG, Django sirve archivos estáticos y media
# En producción, esto debe ser manejado por el servidor web (nginx, Apache)
if settings.DEBUG:
    # Agregar ruta para servir archivos estáticos (/static/)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
    # Nota: Si se usan archivos media (uploads), agregar también:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
