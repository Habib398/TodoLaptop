from django.contrib import admin
from .models import Servicio, ServicioPagado, ProductoServicioPagado

# Register your models here.

class ProductoServicioPagadoInline(admin.TabularInline):
    model = ProductoServicioPagado
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo', 'fecha')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha',)
    ordering = ('-fecha',)

@admin.register(ServicioPagado)
class ServicioPagadoAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'nombre_cliente', 'precio_total', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion', 'servicio')
    search_fields = ('nombre_cliente', 'servicio__nombre')
    readonly_fields = ('precio_total', 'fecha_creacion', 'fecha_pago')
    inlines = [ProductoServicioPagadoInline]
    
    fieldsets = (
        ('Información del Servicio', {
            'fields': ('servicio', 'nombre_cliente', 'estado')
        }),
        ('Precios', {
            'fields': ('precio_servicio', 'precio_productos', 'precio_total')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_pago'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductoServicioPagado)
class ProductoServicioPagadoAdmin(admin.ModelAdmin):
    list_display = ('servicio_pagado', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('servicio_pagado__estado', 'producto')
    search_fields = ('servicio_pagado__nombre_cliente', 'producto__nombre')
