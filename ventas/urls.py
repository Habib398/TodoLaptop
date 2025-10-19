from django.urls import path
from .views import ventas_view, cobrar_productos, cobrar_servicios, buscar_producto

urlpatterns = [
    path('', ventas_view, name='ventas'),
    path('cobrar-productos/', cobrar_productos, name='ventas_cobrar_productos'),
    path('cobrar-servicios/', cobrar_servicios, name='ventas_cobrar_servicios'),
    path('buscar-producto/', buscar_producto, name='buscar_producto'),
]
