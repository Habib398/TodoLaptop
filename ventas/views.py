from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from inventario.models import Producto
from .models import Venta, DetalleVenta
import json


@login_required
def ventas_view(request):
    """Vista principal de Ventas: muestra las opciones para cobrar productos o servicios."""
    return render(request, 'ventas/Ventas.html')


@login_required
def cobrar_productos(request):
    """Vista para cobrar productos - Punto de Venta."""
    if request.method == 'POST':
        try:
            # Obtener los datos del carrito desde el formulario
            carrito_json = request.POST.get('carrito_data', '[]')
            carrito = json.loads(carrito_json)
            
            if not carrito:
                messages.error(request, 'El carrito está vacío.')
                return redirect('ventas_cobrar_productos')
            
            # Crear la venta con transacción atómica
            with transaction.atomic():
                # Crear la venta
                venta = Venta.objects.create(
                    usuario=request.user,
                    metodo_pago='efectivo'
                )
                
                total_venta = 0
                
                # Procesar cada item del carrito
                for item in carrito:
                    producto = get_object_or_404(Producto, id=item['producto_id'])
                    cantidad = int(item['cantidad'])
                    
                    # Verificar stock disponible
                    if producto.cantidad_stock < cantidad:
                        raise ValueError(f'Stock insuficiente para {producto.nombre}. Disponible: {producto.cantidad_stock}')
                    
                    # Crear detalle de venta
                    detalle = DetalleVenta.objects.create(
                        venta=venta,
                        producto=producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                        subtotal=cantidad * producto.precio
                    )
                    
                    # Actualizar stock
                    producto.cantidad_stock -= cantidad
                    producto.save()
                    
                    total_venta += detalle.subtotal
                
                # Actualizar el total de la venta
                venta.total = total_venta
                venta.save()
                
                messages.success(request, f'Venta #{venta.id} realizada con éxito. Total: ${total_venta:.2f}')
                return redirect('ventas_cobrar_productos')
                
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('ventas_cobrar_productos')
        except Exception as e:
            messages.error(request, f'Error al procesar la venta: {str(e)}')
            return redirect('ventas_cobrar_productos')
    
    # GET request - mostrar el formulario
    productos = Producto.objects.filter(cantidad_stock__gt=0).order_by('nombre')
    return render(request, 'ventas/cobrar_productos.html', {
        'productos': productos
    })


@login_required
def buscar_producto(request):
    """Vista AJAX para buscar productos por nombre."""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'productos': []})
    
    productos = Producto.objects.filter(
        nombre__icontains=query,
        cantidad_stock__gt=0
    ).values('id', 'nombre', 'precio', 'cantidad_stock')[:10]
    
    return JsonResponse({'productos': list(productos)})


@login_required
def cobrar_servicios(request):
    """Vista para cobrar servicios (ServicioPagado)."""
    return render(request, 'ventas/cobrar_servicios.html')