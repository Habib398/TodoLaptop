from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm

# ==================== VISTA PRINCIPAL DE INVENTARIO ====================

def inventario_view(request):
    """
    Vista principal que muestra el listado de productos del inventario.
    
    Funcionalidades:
    - Lista todos los productos disponibles
    - Permite buscar productos por nombre (búsqueda insensible a mayúsculas/minúsculas)
    - Ordena los productos alfabéticamente por nombre
    - Incluye un formulario para agregar productos rápidamente
    
    Args:
        request: Objeto HttpRequest con los datos de la petición
        
    Returns:
        HttpResponse: Renderiza la plantilla de inventario con el listado de productos
    """
    # Obtener el término de búsqueda desde los parámetros GET
    # Si no existe, usar cadena vacía y eliminar espacios en blanco
    buscar = request.GET.get("buscar", "").strip()
    
    # Obtener todos los productos de la base de datos
    productos = Producto.objects.all()
    
    # Si hay término de búsqueda, filtrar productos que contengan el término en su nombre
    # icontains: búsqueda case-insensitive (ignora mayúsculas/minúsculas)
    if buscar:
        productos = productos.filter(nombre__icontains=buscar)
    
    # Ordenar los productos alfabéticamente por nombre
    productos = productos.order_by("nombre")
    
    # Crear una instancia del formulario para agregar productos
    form_agregar = ProductoForm()
    
    # Renderizar la plantilla con los datos
    return render(request, "inventario/inventario.html", {
        "productos": productos, 
        "buscar": buscar, 
        "form_agregar": form_agregar
    })


# ==================== AGREGAR PRODUCTO ====================

def agregar_producto(request):
    """
    Vista para agregar un nuevo producto al inventario.
    
    Maneja tanto la visualización del formulario vacío (GET) como el procesamiento
    de los datos enviados (POST). Valida los datos antes de guardar y muestra
    mensajes de éxito al usuario.
    
    Args:
        request: Objeto HttpRequest con los datos de la petición
        
    Returns:
        HttpResponse: Redirige al inventario si es exitoso, o muestra el formulario con errores
    """
    # Verificar si la petición es POST (envío de formulario)
    if request.method == "POST":
        # Crear formulario con los datos enviados
        form = ProductoForm(request.POST)
        
        # Validar los datos del formulario
        if form.is_valid():
            # Guardar el nuevo producto en la base de datos
            form.save()
            
            # Mostrar mensaje de éxito al usuario
            messages.success(request, "Producto agregado correctamente.")
            
            # Redirigir a la vista principal del inventario
            return redirect("inventario")
    else:
        # Si es GET, crear un formulario vacío
        form = ProductoForm()
    
    # Renderizar el formulario (ya sea vacío o con errores)
    return render(request, "inventario/form_producto.html", {
        "form": form, 
        "accion": "Agregar"
    })


# ==================== MODIFICAR PRODUCTO ====================

def modificar_producto(request, pk):
    """
    Vista para modificar un producto existente del inventario.
    
    Busca el producto por su ID (pk) y permite editarlo. Si el producto no existe,
    retorna un error 404. Valida los cambios antes de guardar.
    
    Args:
        request: Objeto HttpRequest con los datos de la petición
        pk: Primary key (ID) del producto a modificar
        
    Returns:
        HttpResponse: Redirige al inventario si es exitoso, o muestra el formulario con datos
    """
    # Buscar el producto por su ID, o retornar 404 si no existe
    producto = get_object_or_404(Producto, pk=pk)
    
    # Verificar si la petición es POST (envío de formulario)
    if request.method == "POST":
        # Crear formulario con los datos enviados y la instancia del producto a modificar
        form = ProductoForm(request.POST, instance=producto)
        
        # Validar los datos del formulario
        if form.is_valid():
            # Guardar los cambios en la base de datos
            form.save()
            
            # Mostrar mensaje de éxito al usuario
            messages.success(request, "Producto modificado correctamente.")
            
            # Redirigir a la vista principal del inventario
            return redirect("inventario")
    else:
        # Si es GET, crear formulario pre-llenado con los datos actuales del producto
        form = ProductoForm(instance=producto)
    
    # Renderizar el formulario (pre-llenado o con errores)
    return render(request, "inventario/form_producto.html", {
        "form": form, 
        "accion": "Modificar"
    })


# ==================== ELIMINAR PRODUCTO ====================

def eliminar_producto(request, pk):
    """
    Vista para eliminar un producto del inventario.
    
    Implementa el patrón de confirmación antes de eliminar. Muestra una página
    de confirmación (GET) y procesa la eliminación definitiva (POST).
    
    Args:
        request: Objeto HttpRequest con los datos de la petición
        pk: Primary key (ID) del producto a eliminar
        
    Returns:
        HttpResponse: Redirige al inventario si se elimina, o muestra página de confirmación
    """
    # Buscar el producto por su ID, o retornar 404 si no existe
    producto = get_object_or_404(Producto, pk=pk)
    
    # Verificar si la petición es POST (confirmación de eliminación)
    if request.method == "POST":
        # Eliminar el producto de la base de datos
        producto.delete()
        
        # Mostrar mensaje de éxito al usuario
        messages.success(request, "Producto eliminado correctamente.")
        
        # Redirigir a la vista principal del inventario
        return redirect("inventario")
    
    # Si es GET, mostrar página de confirmación con los datos del producto
    return render(request, "inventario/confirmar_eliminar.html", {
        "producto": producto
    })