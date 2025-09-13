from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from inventario import views
from usuarios.views import dashboard, login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticación
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),

    # Redirección raíz -> login
    path("", lambda request: redirect("login")),

    # Inventario CRUD
    path("inventario/", views.inventario_view, name="inventario"),
    path("inventario/agregar/", views.agregar_producto, name="agregar_producto"),
    path("inventario/modificar/<int:pk>/", views.modificar_producto, name="modificar_producto"),
    path("inventario/eliminar/<int:pk>/", views.eliminar_producto, name="eliminar_producto"),
]
