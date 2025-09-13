from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm

# Listar productos
def inventario_view(request):
    buscar = request.GET.get("buscar", "").strip()
    productos = Producto.objects.all()
    if buscar:
        productos = productos.filter(nombre__icontains=buscar)
    productos = productos.order_by("nombre")
    form_agregar = ProductoForm()
    return render(request, "inventario/inventario.html", {"productos": productos, "buscar": buscar, "form_agregar": form_agregar})

# Agregar producto
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto agregado correctamente.")
            return redirect("inventario")
    else:
        form = ProductoForm()
    return render(request, "inventario/form_producto.html", {"form": form, "accion": "Agregar"})

# Modificar producto
def modificar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto modificado correctamente.")
            return redirect("inventario")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "inventario/form_producto.html", {"form": form, "accion": "Modificar"})

# Eliminar producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("inventario")
    return render(request, "inventario/confirmar_eliminar.html", {"producto": producto})