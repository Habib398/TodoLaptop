from django.db import models
from usuarios.models import Usuario
from inventario.models import Producto

class Servicio(models.Model):
    nombre = models.CharField(max_length=200, default='Servicio sin nombre')
    tecnico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'rol': 'tecnico'})
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, blank=True)

    def __str__(self):
        return self.nombre


class ServicioPagado(models.Model):
    ESTADO_CHOICES = [
        ('cotizado', 'Cotizado'),
        ('pagado', 'Pagado'),
    ]
    
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=200)
    precio_servicio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_productos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='cotizado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.servicio.nombre} - {self.nombre_cliente} ({self.estado})"

    class Meta:
        verbose_name = "Servicio Pagado"
        verbose_name_plural = "Servicios Pagados"


class ProductoServicioPagado(models.Model):
    servicio_pagado = models.ForeignKey(ServicioPagado, on_delete=models.CASCADE, related_name='productos_utilizados')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    class Meta:
        verbose_name = "Producto en Servicio"
        verbose_name_plural = "Productos en Servicios"

