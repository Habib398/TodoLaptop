from django.db import models
from usuarios.models import Usuario
from inventario.models import Producto

class Servicio(models.Model):
    tecnico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol': 'tecnico'})
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, blank=True)

    def __str__(self):
        return f"Servicio #{self.id}"

