from django.contrib import admin
from .models import Servicio, ServicioPagado, ProductoServicioPagado

# ==================== CONFIGURACIÓN ADMIN AVANZADA ====================

# ==================== INLINE: PRODUCTOS EN SERVICIOS ====================

class ProductoServicioPagadoInline(admin.TabularInline):
    """
    Inline para mostrar productos utilizados dentro de un ServicioPagado.
    
    Permite ver y editar los productos asociados a un servicio directamente
    desde la página de edición del ServicioPagado en el admin de Django.
    
    Características:
    - Formato tabular (más compacto que StackedInline)
    - No muestra filas vacías extras por defecto (extra=0)
    - Campo 'subtotal' de solo lectura (es una propiedad calculada)
    """
    model = ProductoServicioPagado
    extra = 0  # No mostrar formularios vacíos adicionales
    readonly_fields = ('subtotal',)  # Subtotal se calcula automáticamente


# ==================== ADMIN: SERVICIO ====================

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    """
    Configuración personalizada del admin para el modelo Servicio.
    
    Optimiza la visualización y gestión de servicios en el panel de administración,
    incluyendo columnas personalizadas, búsqueda, filtros y ordenamiento.
    """
    
    # Columnas a mostrar en la lista principal
    list_display = ('nombre', 'costo', 'fecha')
    
    # Campos por los que se puede buscar
    search_fields = ('nombre', 'descripcion')
    
    # Filtros laterales disponibles
    list_filter = ('fecha',)
    
    # Ordenamiento por defecto (más recientes primero)
    ordering = ('-fecha',)


# ==================== ADMIN: SERVICIO PAGADO ====================

@admin.register(ServicioPagado)
class ServicioPagadoAdmin(admin.ModelAdmin):
    """
    Configuración personalizada del admin para ServicioPagado.
    
    Proporciona una interfaz completa para gestionar cotizaciones y servicios pagados,
    con visualización detallada de precios, estados y productos utilizados.
    
    Características especiales:
    - Inline de productos para ver materiales utilizados
    - Fieldsets organizados por categorías
    - Campos calculados de solo lectura
    - Filtros múltiples para búsquedas avanzadas
    """
    
    # Columnas a mostrar en la lista principal
    list_display = ('servicio', 'nombre_cliente', 'precio_total', 'estado', 'fecha_creacion')
    
    # Filtros laterales disponibles
    list_filter = ('estado', 'fecha_creacion', 'servicio')
    
    # Campos por los que se puede buscar
    search_fields = ('nombre_cliente', 'servicio__nombre')
    
    # Campos que no pueden ser editados (se calculan o generan automáticamente)
    readonly_fields = ('precio_total', 'fecha_creacion', 'fecha_pago')
    
    # Incluir inline de productos utilizados
    inlines = [ProductoServicioPagadoInline]
    
    # Organizar campos en secciones colapsables
    fieldsets = (
        # Sección: Información básica del servicio
        ('Información del Servicio', {
            'fields': ('servicio', 'nombre_cliente', 'estado')
        }),
        # Sección: Desglose de precios
        ('Precios', {
            'fields': ('precio_servicio', 'precio_productos', 'precio_total')
        }),
        # Sección: Fechas (colapsada por defecto)
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_pago'),
            'classes': ('collapse',)  # Sección colapsable
        }),
    )


# ==================== ADMIN: PRODUCTO EN SERVICIO ====================

@admin.register(ProductoServicioPagado)
class ProductoServicioPagadoAdmin(admin.ModelAdmin):
    """
    Configuración personalizada del admin para ProductoServicioPagado.
    
    Permite gestionar individualmente los registros de productos utilizados
    en servicios, con visualización de cantidades, precios y subtotales.
    """
    
    # Columnas a mostrar en la lista principal
    list_display = ('servicio_pagado', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    
    # Filtros laterales disponibles
    list_filter = ('servicio_pagado__estado', 'producto')
    
    # Campos por los que se puede buscar
    # Nota: __ permite buscar en campos de modelos relacionados
    search_fields = ('servicio_pagado__nombre_cliente', 'producto__nombre')
