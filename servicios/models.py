from django.db import models
from usuarios.models import Usuario
from inventario.models import Producto

# ==================== MODELO PRINCIPAL: SERVICIO ====================

class Servicio(models.Model):
    """
    Modelo que representa un tipo de servicio ofrecido por la empresa.
    
    Define los servicios disponibles en el catálogo (ej: "Reparación de laptop",
    "Instalación de Windows", etc.). Cada servicio tiene un precio base y puede
    requerir productos adicionales del inventario.
    """
    
    # Nombre identificativo del servicio (máximo 200 caracteres)
    # Ejemplo: "Reparación de pantalla laptop"
    nombre = models.CharField(max_length=200, default='Servicio sin nombre')
    
    # Técnico asignado al servicio (opcional)
    # SET_NULL: Si se elimina el técnico, el servicio se mantiene pero sin técnico
    # limit_choices_to: Solo permite seleccionar usuarios con rol 'tecnico'
    tecnico = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'rol': 'tecnico'}
    )
    
    # Descripción detallada del servicio
    descripcion = models.TextField()
    
    # Precio base del servicio (sin incluir productos adicionales)
    # Máximo: 99999999.99
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Fecha de creación del servicio (se asigna automáticamente)
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Relación Many-to-Many con productos del inventario
    # Permite asociar productos que típicamente se usan en este servicio
    productos = models.ManyToManyField(Producto, blank=True)

    def __str__(self):
        """Representación en string del servicio."""
        return self.nombre


# ==================== MODELO: SERVICIO PAGADO/COTIZADO ====================

class ServicioPagado(models.Model):
    """
    Modelo que representa una cotización o venta de servicio a un cliente.
    
    Registra cada vez que se cotiza o vende un servicio, almacenando:
    - Cliente que solicita el servicio
    - Precios desglosados (servicio + productos)
    - Estado actual (cotizado o pagado)
    - Productos específicos utilizados
    
    Este modelo permite hacer seguimiento desde la cotización hasta el pago final.
    """
    
    # Opciones de estado del servicio
    ESTADO_CHOICES = [
        ('cotizado', 'Cotizado'),  # Presupuesto generado, pendiente de pago
        ('pagado', 'Pagado'),      # Servicio pagado y confirmado
    ]
    
    # Relación con el tipo de servicio realizado
    # CASCADE: Si se elimina el servicio base, se eliminan también sus registros de venta
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    
    # Nombre del cliente que solicita el servicio
    nombre_cliente = models.CharField(max_length=200)
    
    # Precio del servicio base (se guarda para mantener historial)
    precio_servicio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Suma total de los productos utilizados
    precio_productos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Precio total = precio_servicio + precio_productos
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Estado actual del servicio (cotizado o pagado)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='cotizado')
    
    # Fecha en que se creó la cotización
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Fecha en que se realizó el pago (null si aún está cotizado)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        """
        Representación en string del servicio pagado.
        Formato: "Nombre Servicio - Cliente (estado)"
        """
        return f"{self.servicio.nombre} - {self.nombre_cliente} ({self.estado})"

    class Meta:
        verbose_name = "Servicio Pagado"
        verbose_name_plural = "Servicios Pagados"


# ==================== MODELO: PRODUCTO EN SERVICIO ====================

class ProductoServicioPagado(models.Model):
    """
    Modelo intermedio que relaciona productos con servicios pagados/cotizados.
    
    Registra qué productos específicos se utilizaron en cada servicio,
    incluyendo cantidad y precio al momento de la venta. Esto permite:
    - Mantener historial de precios (aunque el precio del producto cambie después)
    - Calcular el costo total de productos por servicio
    - Generar reportes detallados de materiales utilizados
    """
    
    # Relación con el servicio pagado/cotizado
    # CASCADE: Si se elimina el servicio, se eliminan también sus productos
    # related_name: Permite acceder desde ServicioPagado.productos_utilizados
    servicio_pagado = models.ForeignKey(
        ServicioPagado, 
        on_delete=models.CASCADE, 
        related_name='productos_utilizados'
    )
    
    # Relación con el producto del inventario
    # CASCADE: Si se elimina el producto, se eliminan también estos registros
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    
    # Cantidad de unidades utilizadas del producto
    cantidad = models.PositiveIntegerField(default=1)
    
    # Precio del producto al momento de la venta/cotización
    # Se guarda para mantener consistencia aunque el precio cambie después
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        """
        Representación en string del producto en servicio.
        Formato: "Nombre Producto x Cantidad"
        """
        return f"{self.producto.nombre} x{self.cantidad}"
    
    @property
    def subtotal(self):
        """
        Calcula el subtotal del producto en el servicio.
        
        Returns:
            Decimal: cantidad * precio_unitario
        """
        return self.cantidad * self.precio_unitario

    class Meta:
        verbose_name = "Producto en Servicio"
        verbose_name_plural = "Productos en Servicios"

