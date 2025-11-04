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

# ==================== VISTAS CRUD BÁSICAS ====================

@login_required
def agregar_servicio(request):
    """
    Vista para agregar un nuevo tipo de servicio al catálogo.
    
    Crea un nuevo servicio base que podrá ser cotizado posteriormente.
    Valida que todos los campos obligatorios estén presentes y que el
    costo sea un número válido.
    
    Args:
        request: Objeto HttpRequest con los datos del formulario POST
        
    Returns:
        HttpResponse: Redirige a la vista de servicios con mensaje de éxito/error
    """
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        costo = request.POST.get('costo_servicio', 0)
        
        # Validar que todos los campos estén presentes
        if nombre and descripcion and costo:
            try:
                # Crear el nuevo servicio
                servicio = Servicio(
                    nombre=nombre,
                    descripcion=descripcion,
                    costo=float(costo)
                )
                servicio.save()
                
                # Mensaje de éxito con detalles del servicio creado
                messages.success(request, f'Servicio "{servicio.nombre}" creado exitosamente - ${servicio.costo}')
                return redirect('servicios')
                
            except Exception as e:
                # Capturar errores de conversión de tipo o de base de datos
                messages.error(request, f'Error al crear el servicio: {str(e)}')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    
    return redirect('servicios')


@login_required
def modificar_servicio(request, pk):
    """
    Vista para modificar un servicio existente del catálogo.
    
    Actualiza los datos de un servicio. Si el servicio no existe,
    retorna un error 404.
    
    Args:
        request: Objeto HttpRequest con los datos del formulario POST
        pk: Primary key (ID) del servicio a modificar
        
    Returns:
        HttpResponse: Redirige a la vista de servicios con mensaje de éxito/error
    """
    # Buscar el servicio o retornar 404 si no existe
    try:
        servicio = Servicio.objects.get(pk=pk)
    except Servicio.DoesNotExist:
        raise Http404('Servicio no encontrado')
    
    if request.method == 'POST':
        # Actualizar los campos del servicio
        # Si no se proporciona un valor, mantiene el valor actual
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
    """
    Vista para eliminar un servicio del catálogo.
    
    Elimina permanentemente un servicio de la base de datos.
    NOTA: Debido al CASCADE, también eliminará todos los ServicioPagado asociados.
    
    Args:
        request: Objeto HttpRequest con confirmación POST
        pk: Primary key (ID) del servicio a eliminar
        
    Returns:
        HttpResponse: Redirige a la vista de servicios con mensaje de éxito/error
    """
    # Buscar el servicio o retornar 404 si no existe
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


# ==================== VISTA PRINCIPAL DE SERVICIOS ====================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Servicio
from usuarios.models import Usuario
from inventario.models import Producto

@login_required
def servicios_view(request):
    """
    Vista principal que muestra el catálogo de servicios disponibles.
    
    Funcionalidades:
    - Lista todos los servicios ordenados por fecha de creación (más recientes primero)
    - Permite crear nuevos servicios (solo para admins)
    - Opción de cotizar servicios (disponible para todos los usuarios)
    - Procesamiento de formularios para múltiples acciones
    
    Args:
        request: Objeto HttpRequest con posible formulario POST
        
    Returns:
        HttpResponse: Renderiza la plantilla de servicios con el listado completo
    """
    
    # ========== Procesar formularios POST ==========
    if request.method == 'POST':
        # Identificar qué acción se está solicitando
        action = request.POST.get('action')
        
        # --- Acción: COTIZAR ---
        # Disponible para todos los usuarios autenticados
        if action == 'cotizar':
            servicio_id = request.POST.get('servicio_seleccionado')
            
            if servicio_id:
                # Redirigir a la vista de cotización con el servicio seleccionado
                return redirect('cotizar_servicio', servicio_id=servicio_id)
            else:
                messages.error(request, 'Por favor, selecciona un servicio para cotizar.')
        
        # --- Acción: CREAR SERVICIO ---
        # Solo disponible para administradores y superusuarios
        elif action == 'crear' and (request.user.is_staff or request.user.is_superuser):
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            costo_servicio = request.POST.get('costo_servicio', 0)
            
            # Validar campos obligatorios
            if nombre and descripcion and costo_servicio:
                try:
                    # Crear el nuevo servicio
                    servicio = Servicio(
                        nombre=nombre,
                        descripcion=descripcion,
                        costo=float(costo_servicio)
                    )
                    
                    servicio.save()
                    messages.success(request, f'Servicio "{servicio.nombre}" creado exitosamente - ${servicio.costo}')
                    return redirect('servicios')
                    
                except ValueError:
                    # Error al convertir el costo a número
                    messages.error(request, 'Error: El costo debe ser un número válido.')
                except Exception as e:
                    # Otros errores (base de datos, etc.)
                    messages.error(request, f'Error al crear el servicio: {str(e)}')
            else:
                messages.error(request, 'Error: El nombre, descripción y costo son campos requeridos.')
    
    # ========== Obtener datos para mostrar ==========
    # Obtener todos los servicios ordenados por fecha (más recientes primero)
    servicios = Servicio.objects.all().order_by('-fecha')
    
    # Preparar contexto para la plantilla
    context = {
        'servicios': servicios,
    }
    
    return render(request, 'servicios/servicios.html', context)


# ==================== VISTA DE COTIZACIÓN ====================

@login_required
def cotizar_servicio(request, servicio_id):
    """
    Vista para generar una cotización de un servicio específico.
    
    Permite crear una cotización que incluye:
    - El servicio base seleccionado
    - Productos adicionales del inventario (opcional)
    - Cálculo automático de totales
    - Guardado como ServicioPagado con estado 'cotizado'
    
    El flujo es:
    1. Mostrar formulario con servicio y productos disponibles (GET)
    2. Procesar cotización y guardar en BD (POST)
    
    Args:
        request: Objeto HttpRequest con posible formulario POST
        servicio_id: ID del servicio a cotizar
        
    Returns:
        HttpResponse: Renderiza formulario de cotización o redirige tras guardar
    """
    # Obtener el servicio a cotizar o retornar 404
    servicio = get_object_or_404(Servicio, id=servicio_id)
    
    # Obtener productos disponibles (con stock mayor a 0) ordenados alfabéticamente
    productos = Producto.objects.filter(cantidad_stock__gt=0).order_by('nombre')
    
    if request.method == 'POST':
        try:
            # ========== Obtener datos del formulario ==========
            nombre_cliente = request.POST.get('nombre_cliente')
            
            # Los productos vienen en formato JSON desde JavaScript
            productos_data = json.loads(request.POST.get('productos_json', '[]'))
            
            # Validar que el nombre del cliente esté presente
            if not nombre_cliente:
                messages.error(request, 'El nombre del cliente es obligatorio.')
                return redirect('cotizar_servicio', servicio_id=servicio_id)
            
            # ========== Calcular totales ==========
            precio_productos = 0
            
            # Sumar el precio de todos los productos seleccionados
            for item in productos_data:
                producto = Producto.objects.get(id=item['producto_id'])
                precio_productos += float(producto.precio) * int(item['cantidad'])
            
            # Precio total = servicio base + productos
            precio_total = float(servicio.costo) + precio_productos
            
            # ========== Crear el registro de servicio cotizado ==========
            servicio_pagado = ServicioPagado.objects.create(
                servicio=servicio,
                nombre_cliente=nombre_cliente,
                precio_servicio=servicio.costo,
                precio_productos=precio_productos,
                precio_total=precio_total,
                estado='cotizado'  # Estado inicial
            )
            
            # ========== Agregar productos utilizados ==========
            # Crear registros individuales para cada producto en la cotización
            for item in productos_data:
                producto = Producto.objects.get(id=item['producto_id'])
                ProductoServicioPagado.objects.create(
                    servicio_pagado=servicio_pagado,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_unitario=producto.precio  # Guardar precio actual
                )
            
            # Mensaje de éxito con total de la cotización
            messages.success(request, f'Cotización creada exitosamente. Total: ${precio_total:.2f}')
            return redirect('servicios')
            
        except Exception as e:
            # Capturar cualquier error durante el proceso
            messages.error(request, f'Error al crear la cotización: {str(e)}')
    
    # ========== Preparar contexto para el formulario ==========
    context = {
        'servicio': servicio,
        'productos': productos,
    }
    
    return render(request, 'servicios/cotizar.html', context)


# ==================== VISTA AJAX PARA INFORMACIÓN DE PRODUCTOS ====================

@csrf_exempt
@login_required
def obtener_producto_info(request):
    """
    Vista AJAX que retorna información de un producto específico.
    
    Utilizada desde JavaScript para obtener datos del producto sin recargar
    la página. Útil para mostrar información dinámica al seleccionar productos.
    
    Args:
        request: Objeto HttpRequest POST con producto_id
        
    Returns:
        JsonResponse: Datos del producto (nombre, precio, stock) o error
    """
    if request.method == 'POST':
        try:
            # Obtener el ID del producto desde el POST
            producto_id = request.POST.get('producto_id')
            
            # Buscar el producto en la base de datos
            producto = Producto.objects.get(id=producto_id)
            
            # Preparar respuesta JSON con los datos del producto
            data = {
                'success': True,
                'nombre': producto.nombre,
                'precio': str(producto.precio),  # Convertir a string para JSON
                'stock': producto.cantidad_stock
            }
            
            return JsonResponse(data)
            
        except Producto.DoesNotExist:
            # Producto no encontrado en la base de datos
            return JsonResponse({
                'success': False, 
                'error': 'Producto no encontrado'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
