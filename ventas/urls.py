from django.urls import path
from .views import ventas_view, cobrar_productos, cobrar_servicios, buscar_producto, pagar_servicio

urlpatterns = [
    path('', ventas_view, name='ventas'),
    path('cobrar-productos/', cobrar_productos, name='ventas_cobrar_productos'),
    path('cobrar-servicios/', cobrar_servicios, name='ventas_cobrar_servicios'),
    path('pagar-servicio/<int:servicio_id>/', pagar_servicio, name='pagar_servicio'),
    path('buscar-producto/', buscar_producto, name='buscar_producto'),
]
