"""
Modelos del módulo de ventas.

Este módulo define los modelos para el registro de ventas de productos
del sistema TodoLap. Implementa un sistema de punto de venta (POS) con
ventas y sus detalles.

MODELOS:
- Venta: Encabezado de la venta con información general
- DetalleVenta: Líneas de detalle de productos vendidos
"""

from django.db import models
from usuarios.models import Usuario
from inventario.models import Producto

# ==================== MODELO: VENTA ====================

class Venta(models.Model):
    """
    Modelo que representa una venta realizada en el sistema.
    
    Almacena el encabezado de la transacción de venta con información
    general como el usuario que realizó la venta, fecha, total y método
    de pago.
    
    RELACIONES:
    - Usuario: Usuario que registra la venta (puede ser null si se elimina)
    - DetalleVenta: Productos vendidos (relación inversa 'detalles')
    
    CAMPOS:
    - usuario: Usuario que realiza la venta (SET_NULL al eliminar)
    - fecha: Fecha y hora de la venta (auto-asignada)
    - total: Monto total de la venta (calculado desde detalles)
    - metodo_pago: Forma de pago (efectivo por defecto)
    
    MÉTODOS:
    - calcular_total(): Suma los subtotales de los detalles
    
    USO:
        venta = Venta.objects.create(usuario=user, metodo_pago='efectivo')
        venta.calcular_total()  # Actualiza el total
    """
    
    # Usuario que realiza la venta
    # SET_NULL: Si se elimina el usuario, la venta permanece pero sin referencia
    # limit_choices_to: Originalmente limitado a 'cajero', pero acepta cualquier usuario
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'rol': 'cajero'}
    )
    
    # Fecha y hora de la venta (se asigna automáticamente al crear)
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Total de la venta (se calcula sumando los detalles)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Método de pago utilizado
    metodo_pago = models.CharField(max_length=20, default='efectivo')
    
    def __str__(self):
        """Representación en string del modelo."""
        return f"Venta #{self.id} - ${self.total}"
    
    def calcular_total(self):
        """
        Calcula el total de la venta sumando los subtotales de los detalles.
        
        Este método recorre todos los DetalleVenta asociados, suma sus
        subtotales, actualiza el campo total y guarda el objeto.
        
        Returns:
            Decimal: Total calculado de la venta
        """
        # Sumar todos los subtotales de los detalles relacionados
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        
        # Actualizar el campo total
        self.total = total
        
        # Guardar en la base de datos
        self.save()
        
        return total

# ==================== MODELO: DETALLE DE VENTA ====================

class DetalleVenta(models.Model):
    """
    Modelo que representa una línea de detalle de una venta.
    
    Cada instancia representa un producto vendido dentro de una venta,
    con su cantidad, precio unitario y subtotal calculado.
    
    RELACIONES:
    - Venta: Venta a la que pertenece (CASCADE al eliminar)
    - Producto: Producto vendido (CASCADE al eliminar)
    
    CAMPOS:
    - venta: Venta asociada
    - producto: Producto vendido
    - cantidad: Unidades vendidas
    - precio_unitario: Precio del producto al momento de la venta
    - subtotal: Total de la línea (cantidad × precio_unitario)
    
    CÁLCULO AUTOMÁTICO:
    El subtotal se calcula automáticamente en el método save()
    
    USO:
        detalle = DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=2,
            precio_unitario=producto.precio
        )
        # El subtotal se calcula automáticamente: 2 × precio
    """
    
    # Venta a la que pertenece este detalle
    # CASCADE: Si se elimina la venta, se eliminan todos sus detalles
    # related_name='detalles': Permite acceder desde Venta con venta.detalles.all()
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    
    # Producto vendido
    # CASCADE: Si se elimina el producto, se elimina el detalle (cuidado en producción)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    # Cantidad de unidades vendidas (solo números positivos)
    cantidad = models.PositiveIntegerField()
    
    # Precio del producto al momento de la venta
    # Se guarda para mantener histórico (el precio del producto puede cambiar)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Subtotal de esta línea (cantidad × precio_unitario)
    # Se calcula automáticamente en save()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Representación en string del modelo."""
        return f"{self.producto.nombre} x{self.cantidad}"
    
    def save(self, *args, **kwargs):
        """
        Calcula el subtotal automáticamente antes de guardar.
        
        Sobrescribe el método save() para calcular el subtotal
        multiplicando cantidad por precio_unitario antes de
        persistir en la base de datos.
        
        Args:
            *args: Argumentos posicionales
            **kwargs: Argumentos con nombre
        """
        # Calcular subtotal: cantidad × precio unitario
        self.subtotal = self.cantidad * self.precio_unitario
        
        # Llamar al método save() original
        super().save(*args, **kwargs)
