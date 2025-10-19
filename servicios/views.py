from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Servicio, ServicioPagado, ProductoServicioPagado
from usuarios.models import Usuario
from inventario.models import Producto

@login_required
def agregar_servicio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        costo = request.POST.get('costo_servicio', 0)
        if nombre and descripcion and costo:
            try:
                servicio = Servicio(
                    nombre=nombre,
                    descripcion=descripcion,
                    costo=float(costo)
                )
                servicio.save()
                messages.success(request, f'Servicio "{servicio.nombre}" creado exitosamente - ${servicio.costo}')
                return redirect('servicios')
            except Exception as e:
                messages.error(request, f'Error al crear el servicio: {str(e)}')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    return redirect('servicios')

@login_required
def modificar_servicio(request, pk):
    try:
        servicio = Servicio.objects.get(pk=pk)
    except Servicio.DoesNotExist:
        raise Http404('Servicio no encontrado')
    if request.method == 'POST':
        servicio.nombre = request.POST.get('nombre', servicio.nombre)
        servicio.descripcion = request.POST.get('descripcion', servicio.descripcion)
        servicio.costo = request.POST.get('costo_servicio', servicio.costo)
        try:
            servicio.save()
            messages.success(request, f'Servicio "{servicio.nombre}" modificado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al modificar el servicio: {str(e)}')
        return redirect('servicios')
    return redirect('servicios')

@login_required
def eliminar_servicio(request, pk):
    try:
        servicio = Servicio.objects.get(pk=pk)
    except Servicio.DoesNotExist:
        raise Http404('Servicio no encontrado')
    if request.method == 'POST':
        try:
            servicio.delete()
            messages.success(request, f'Servicio eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el servicio: {str(e)}')
        return redirect('servicios')
    return redirect('servicios')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Servicio
from usuarios.models import Usuario
from inventario.models import Producto

@login_required
def servicios_view(request):
    """Vista principal de servicios con dropdown y opción de crear servicios para admins"""
    
    # Procesar formularios
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Acción de cotizar (disponible para todos los usuarios)
        if action == 'cotizar':
            servicio_id = request.POST.get('servicio_seleccionado')
            if servicio_id:
                # Redirigir a la vista de cotización
                return redirect('cotizar_servicio', servicio_id=servicio_id)
            else:
                messages.error(request, 'Por favor, selecciona un servicio para cotizar.')
        
        # Acción de crear servicio (solo para admins)
        elif action == 'crear' and (request.user.is_staff or request.user.is_superuser):
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            costo_servicio = request.POST.get('costo_servicio', 0)
            
            if nombre and descripcion and costo_servicio:
                try:
                    # Crear el servicio
                    servicio = Servicio(
                        nombre=nombre,
                        descripcion=descripcion,
                        costo=float(costo_servicio)
                    )
                    
                    servicio.save()
                    messages.success(request, f'Servicio "{servicio.nombre}" creado exitosamente - ${servicio.costo}')
                    return redirect('servicios')
                    
                except ValueError:
                    messages.error(request, 'Error: El costo debe ser un número válido.')
                except Exception as e:
                    messages.error(request, f'Error al crear el servicio: {str(e)}')
            else:
                messages.error(request, 'Error: El nombre, descripción y costo son campos requeridos.')
    
    # Obtener datos para mostrar
    servicios = Servicio.objects.all().order_by('-fecha')
    
    context = {
        'servicios': servicios,
    }
    return render(request, 'servicios/servicios.html', context)


@login_required
def cotizar_servicio(request, servicio_id):
    """Vista para cotizar un servicio específico"""
    servicio = get_object_or_404(Servicio, id=servicio_id)
    productos = Producto.objects.filter(cantidad_stock__gt=0).order_by('nombre')
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre_cliente = request.POST.get('nombre_cliente')
            productos_data = json.loads(request.POST.get('productos_json', '[]'))
            
            if not nombre_cliente:
                messages.error(request, 'El nombre del cliente es obligatorio.')
                return redirect('cotizar_servicio', servicio_id=servicio_id)
            
            # Calcular totales
            precio_productos = 0
            for item in productos_data:
                producto = Producto.objects.get(id=item['producto_id'])
                precio_productos += float(producto.precio) * int(item['cantidad'])
            
            precio_total = float(servicio.costo) + precio_productos
            
            # Crear el servicio pagado
            servicio_pagado = ServicioPagado.objects.create(
                servicio=servicio,
                nombre_cliente=nombre_cliente,
                precio_servicio=servicio.costo,
                precio_productos=precio_productos,
                precio_total=precio_total,
                estado='cotizado'
            )
            
            # Agregar productos utilizados
            for item in productos_data:
                producto = Producto.objects.get(id=item['producto_id'])
                ProductoServicioPagado.objects.create(
                    servicio_pagado=servicio_pagado,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_unitario=producto.precio
                )
            
            messages.success(request, f'Cotización creada exitosamente. Total: ${precio_total:.2f}')
            return redirect('servicios')
            
        except Exception as e:
            messages.error(request, f'Error al crear la cotización: {str(e)}')
    
    context = {
        'servicio': servicio,
        'productos': productos,
    }
    return render(request, 'servicios/cotizar.html', context)


@csrf_exempt
@login_required
def obtener_producto_info(request):
    """Vista AJAX para obtener información de un producto"""
    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id')
            producto = Producto.objects.get(id=producto_id)
            
            data = {
                'success': True,
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'stock': producto.cantidad_stock
            }
            return JsonResponse(data)
        except Producto.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
