from django.db import models

class Producto(models.Model):
    """
    Modelo que representa un producto en el inventario.
    
    Este modelo almacena la información de los productos disponibles para venta,
    incluyendo su nombre, descripción, precio y cantidad en stock.
    """
    
    # Nombre del producto (máximo 100 caracteres)
    nombre = models.CharField(max_length=100)
    
    # Descripción detallada del producto (campo opcional)
    descripcion = models.TextField(blank=True, null=True)
    
    # Precio del producto (máximo 10 dígitos, 2 decimales)
    # Ejemplo: 99999999.99
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Cantidad disponible en inventario (solo números positivos)
    # Por defecto inicia en 0
    cantidad_stock = models.PositiveIntegerField(verbose_name="Cantidad en stock", default=0)

    def __str__(self):
        """
        Representación en string del producto.
        Retorna el nombre del producto para facilitar su identificación.
        """
        return self.nombre
