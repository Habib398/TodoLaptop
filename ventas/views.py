"""
Vistas del módulo de ventas.

Este módulo contiene todas las vistas para el sistema de ventas:
- Punto de venta (POS) para productos
- Cobro de servicios de reparación
- Búsqueda de productos vía AJAX

VISTAS DISPONIBLES:
- ventas_view: Página principal con opciones
- cobrar_productos: Punto de venta para productos
- buscar_producto: API AJAX para búsqueda
- cobrar_servicios: Gestión de servicios cotizados/pagados
- pagar_servicio: Procesar pago de servicio
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from inventario.models import Producto
from servicios.models import ServicioPagado
from .models import Venta, DetalleVenta
import json

# ==================== VISTA PRINCIPAL ====================

@login_required
def ventas_view(request):
    """
    Vista principal del módulo de Ventas.
    
    Muestra las opciones disponibles:
    - Cobrar productos (Punto de Venta)
    - Cobrar servicios (Servicios completados)
    
    PERMISOS:
    - Requiere autenticación (@login_required)
    
    Args:
        request: Objeto HttpRequest
        
    Returns:
        HttpResponse: Renderiza template con opciones de ventas
    """
    return render(request, 'ventas/Ventas.html')

# ==================== PUNTO DE VENTA (PRODUCTOS) ====================

@login_required
def cobrar_productos(request):
    """
    Vista del Punto de Venta (POS) para cobrar productos.
    
    GET: Muestra la interfaz del punto de venta con productos disponibles
    POST: Procesa la venta del carrito de productos
    
    FLUJO POST:
    1. Recibe datos del carrito en JSON
    2. Valida stock disponible de cada producto
    3. Crea la Venta y sus DetalleVenta
    4. Actualiza el stock de productos
    5. Calcula y guarda el total
    
    CARACTERÍSTICAS:
    - Transacción atómica para integridad de datos
    - Validación de stock antes de procesar
    - Actualización automática de inventario
    - Sistema de carrito con múltiples productos
    
    PERMISOS:
    - Requiere autenticación (@login_required)
    
    Args:
        request: Objeto HttpRequest con carrito_data en POST
        
    Returns:
        HttpResponse: Template del POS o redirección después de venta
    """
    if request.method == 'POST':
        try:
            # Obtener los datos del carrito desde el formulario
            # El JavaScript envía el carrito serializado como JSON
            carrito_json = request.POST.get('carrito_data', '[]')
            carrito = json.loads(carrito_json)
            
            # Validar que el carrito no esté vacío
            if not carrito:
                messages.error(request, 'El carrito está vacío.')
                return redirect('ventas_cobrar_productos')
            
            # Crear la venta con transacción atómica
            # Si algo falla, se revierte toda la operación
            with transaction.atomic():
                # Crear el encabezado de la venta
                venta = Venta.objects.create(
                    usuario=request.user,
                    metodo_pago='efectivo'  # Por ahora solo efectivo
                )
                
                total_venta = 0
                
                # Procesar cada item del carrito
                for item in carrito:
                    # Obtener el producto o retornar 404
                    producto = get_object_or_404(Producto, id=item['producto_id'])
                    cantidad = int(item['cantidad'])
                    
                    # Verificar stock disponible
                    if producto.cantidad_stock < cantidad:
                        raise ValueError(
                            f'Stock insuficiente para {producto.nombre}. '
                            f'Disponible: {producto.cantidad_stock}'
                        )
                    
                    # Crear detalle de venta
                    # El subtotal se calcula automáticamente en save()
                    detalle = DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                        subtotal=cantidad * producto.precio
                    )
                    
                    # Actualizar stock del producto (restar cantidad vendida)
                    producto.cantidad_stock -= cantidad
                    producto.save()
                    
                    # Acumular total de la venta
                    total_venta += detalle.subtotal
                
                # Actualizar el total de la venta
                venta.total = total_venta
                venta.save()
                
                # Mensaje de éxito
                messages.success(
                    request, 
                    f'Venta #{venta.id} realizada con éxito. Total: ${total_venta:.2f}'
                )
                return redirect('ventas_cobrar_productos')
                
        except ValueError as e:
            # Error de validación (stock insuficiente, etc.)
            messages.error(request, str(e))
            return redirect('ventas_cobrar_productos')
        except Exception as e:
            # Error general en el proceso
            messages.error(request, f'Error al procesar la venta: {str(e)}')
            return redirect('ventas_cobrar_productos')
    
    # GET request - mostrar el formulario del punto de venta
    # Filtrar solo productos con stock disponible
    productos = Producto.objects.filter(cantidad_stock__gt=0).order_by('nombre')
    
    return render(request, 'ventas/cobrar_productos.html', {
        'productos': productos
    })

# ==================== API AJAX: BÚSQUEDA DE PRODUCTOS ====================

@login_required
def buscar_producto(request):
    """
    Vista AJAX para buscar productos por nombre.
    
    Proporciona una API para búsqueda en tiempo real de productos
    desde el punto de venta. Retorna datos en formato JSON.
    
    PARÁMETROS GET:
    - q: Término de búsqueda (mínimo 2 caracteres)
    
    FILTROS:
    - Nombre contiene el término (case-insensitive)
    - Solo productos con stock disponible
    - Máximo 10 resultados
    
    RESPUESTA JSON:
    {
        "productos": [
            {
                "id": 1,
                "nombre": "Laptop HP",
                "precio": "15000.00",
                "cantidad_stock": 5
            },
            ...
        ]
    }
    
    PERMISOS:
    - Requiere autenticación (@login_required)
    
    Args:
        request: Objeto HttpRequest con parámetro 'q' en GET
        
    Returns:
        JsonResponse: Lista de productos que coinciden con la búsqueda
    """
    # Obtener término de búsqueda del querystring
    query = request.GET.get('q', '')
    
    # Validar longitud mínima del término de búsqueda
    if len(query) < 2:
        return JsonResponse({'productos': []})
    
    # Buscar productos que coincidan con el término
    # __icontains: búsqueda case-insensitive que contiene el término
    # cantidad_stock__gt=0: solo productos con stock disponible
    productos = Producto.objects.filter(
        nombre__icontains=query,
        cantidad_stock__gt=0
    ).values('id', 'nombre', 'precio', 'cantidad_stock')[:10]
    
    # Retornar JSON con la lista de productos
    return JsonResponse({'productos': list(productos)})

# ==================== COBRO DE SERVICIOS ====================

@login_required
def cobrar_servicios(request):
    """
    Vista para gestionar y cobrar servicios de reparación.
    
    Muestra una lista de servicios con dos estados:
    - Cotizados: Servicios completados pendientes de pago
    - Pagados: Historial de servicios ya cobrados
    
    PARÁMETROS GET:
    - mostrar: 'cotizados' o 'pagados' (default: 'cotizados')
    - q: Término de búsqueda por cliente o servicio
    
    FUNCIONALIDADES:
    - Filtrado por estado (cotizado/pagado)
    - Búsqueda por nombre de cliente o tipo de servicio
    - Vista de detalles de cada servicio
    - Botón para procesar pago de servicios cotizados
    
    PERMISOS:
    - Requiere autenticación (@login_required)
    
    Args:
        request: Objeto HttpRequest con parámetros GET opcionales
        
    Returns:
        HttpResponse: Template con lista de servicios filtrada
    """
    # Obtener el filtro de estado (cotizado o pagado)
    mostrar = request.GET.get('mostrar', 'cotizados')  # Default: cotizados
    query = request.GET.get('q', '')  # Término de búsqueda
    
    # Filtrar según el estado seleccionado
    if mostrar == 'pagados':
        # Mostrar servicios ya pagados (historial)
        servicios = ServicioPagado.objects.filter(
            estado='pagado'
        ).select_related('servicio').order_by('-fecha_pago')
    else:
        # Mostrar servicios cotizados pendientes de pago
        servicios = ServicioPagado.objects.filter(
            estado='cotizado'
        ).select_related('servicio').order_by('-fecha_creacion')
    
    # Filtrar por búsqueda si existe un término
    if query:
        # Buscar por nombre de cliente O por nombre del servicio
        servicios = servicios.filter(
            nombre_cliente__icontains=query
        ) | servicios.filter(
            servicio__nombre__icontains=query
        )
    
    # Preparar contexto para el template
    context = {
        'servicios': servicios,
        'query': query,
        'mostrar': mostrar  # Para mantener el tab activo
    }
    
    return render(request, 'ventas/cobrar_servicios.html', context)

# ==================== PROCESAR PAGO DE SERVICIO ====================

@login_required
def pagar_servicio(request, servicio_id):
    """
    Vista para procesar el pago de un servicio cotizado.
    
    Cambia el estado de un servicio de 'cotizado' a 'pagado' y
    registra la fecha de pago.
    
    FLUJO:
    1. Valida que el servicio exista y esté en estado 'cotizado'
    2. Cambia el estado a 'pagado'
    3. Registra la fecha y hora del pago
    4. Guarda los cambios
    5. Muestra mensaje de confirmación
    
    SEGURIDAD:
    - Solo procesa servicios en estado 'cotizado'
    - Usa transacción atómica para integridad
    
    PERMISOS:
    - Requiere autenticación (@login_required)
    - Solo acepta método POST
    
    Args:
        request: Objeto HttpRequest (debe ser POST)
        servicio_id (int): ID del ServicioPagado a pagar
        
    Returns:
        HttpResponseRedirect: Redirige a la lista de servicios
    """
    if request.method == 'POST':
        try:
            # Usar transacción atómica para integridad de datos
            with transaction.atomic():
                # Obtener el servicio cotizado o retornar 404
                # Solo permite servicios en estado 'cotizado'
                servicio_pagado = get_object_or_404(
                    ServicioPagado, 
                    id=servicio_id, 
                    estado='cotizado'
                )
                
                # Actualizar el estado a pagado
                servicio_pagado.estado = 'pagado'
                
                # Registrar fecha y hora del pago
                servicio_pagado.fecha_pago = timezone.now()
                
                # Guardar cambios en la base de datos
                servicio_pagado.save()
                
                # Mensaje de éxito con detalles
                messages.success(
                    request, 
                    f'Servicio "{servicio_pagado.servicio.nombre}" pagado exitosamente. '
                    f'Total: ${servicio_pagado.precio_total:.2f}'
                )
                return redirect('ventas_cobrar_servicios')
                
        except Exception as e:
            # Error al procesar el pago
            messages.error(request, f'Error al procesar el pago: {str(e)}')
            return redirect('ventas_cobrar_servicios')
    
    # Si no es POST, redirigir a la lista
    return redirect('ventas_cobrar_servicios')
