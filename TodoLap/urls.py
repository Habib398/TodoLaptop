from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventario import views
from usuarios.views import dashboard, login_view, logout_view, agregar_usuario, listar_usuarios, editar_usuario, cambiar_estado_usuario, eliminar_usuario
from servicios.views import servicios_view, agregar_servicio, modificar_servicio, eliminar_servicio, cotizar_servicio, obtener_producto_info

urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticación
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    
    # Gestión de usuarios (solo admin)
    path("usuarios/agregar/", agregar_usuario, name="agregar_usuario"),
    path("usuarios/listar/", listar_usuarios, name="listar_usuarios"),
    path("usuarios/editar/<int:pk>/", editar_usuario, name="editar_usuario"),
    path("usuarios/estado/<int:pk>/", cambiar_estado_usuario, name="cambiar_estado_usuario"),
    path("usuarios/eliminar/<int:pk>/", eliminar_usuario, name="eliminar_usuario"),

    # Redirección raíz -> login
    path("", lambda request: redirect("login")),

    # Inventario CRUD
    path("inventario/", views.inventario_view, name="inventario"),
    path("inventario/agregar/", views.agregar_producto, name="agregar_producto"),
    path("inventario/modificar/<int:pk>/", views.modificar_producto, name="modificar_producto"),
    path("inventario/eliminar/<int:pk>/", views.eliminar_producto, name="eliminar_producto"),
    
    # Servicios
    path("servicios/", servicios_view, name="servicios"),
    path("servicios/agregar/", agregar_servicio, name="agregar_servicio"),
    path("servicios/modificar/<int:pk>/", modificar_servicio, name="modificar_servicio"),
    path("servicios/eliminar/<int:pk>/", eliminar_servicio, name="eliminar_servicio"),
    path("servicios/cotizar/<int:servicio_id>/", cotizar_servicio, name="cotizar_servicio"),
    path("servicios/producto-info/", obtener_producto_info, name="obtener_producto_info"),
    
    # Ventas
    path("ventas/", include('ventas.urls')),
]

# Servir archivos estáticos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
