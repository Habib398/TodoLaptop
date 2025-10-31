from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm
from .models import Usuario

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Debug: ver qué está llegando
        print(f"[DEBUG] Login attempt - Username: {username}")
        print(f"[DEBUG] Request method: {request.method}")
        print(f"[DEBUG] Request origin: {request.headers.get('origin', 'No origin')}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"[DEBUG] Login successful for user: {username}")
            return redirect("dashboard")
        else:
            print(f"[DEBUG] Login failed for user: {username}")
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "usuarios/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "usuarios/dashboard.html")

@login_required
def agregar_usuario(request):
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para acceder a esta página")
        return redirect("dashboard")
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        rol = request.POST.get('rol')
        
        # Validaciones
        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("listar_usuarios")
        
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, f"El usuario '{username}' ya existe")
            return redirect("listar_usuarios")
        
        # Crear usuario
        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            rol=rol
        )
        messages.success(request, f"Usuario '{username}' creado exitosamente")
        return redirect("listar_usuarios")
    
    return redirect("listar_usuarios")

@login_required
def listar_usuarios(request):
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para acceder a esta página")
        return redirect("dashboard")
    
    buscar = request.GET.get('buscar', '')
    if buscar:
        usuarios = Usuario.objects.filter(
            username__icontains=buscar
        ).order_by('-date_joined') | Usuario.objects.filter(
            first_name__icontains=buscar
        ).order_by('-date_joined') | Usuario.objects.filter(
            last_name__icontains=buscar
        ).order_by('-date_joined')
    else:
        usuarios = Usuario.objects.all().order_by('-date_joined')
    
    return render(request, "usuarios/listar_usuarios.html", {
        "usuarios": usuarios,
        "buscar": buscar
    })

@login_required
def editar_usuario(request, pk):
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para realizar esta acción")
        return redirect("dashboard")
    
    try:
        usuario = Usuario.objects.get(pk=pk)
        
        if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            rol = request.POST.get('rol')
            new_password = request.POST.get('new_password')
            new_password_confirm = request.POST.get('new_password_confirm')
            
            # Validar que el username no esté en uso por otro usuario
            if Usuario.objects.filter(username=username).exclude(pk=pk).exists():
                messages.error(request, f"El usuario '{username}' ya está en uso")
                return redirect("listar_usuarios")
            
            # Actualizar datos
            usuario.username = username
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.rol = rol
            
            # Cambiar contraseña si se proporcionó
            if new_password:
                if new_password != new_password_confirm:
                    messages.error(request, "Las contraseñas no coinciden")
                    return redirect("listar_usuarios")
                usuario.set_password(new_password)
            
            usuario.save()
            messages.success(request, f"Usuario '{username}' actualizado exitosamente")
            return redirect("listar_usuarios")
            
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe")
    
    return redirect("listar_usuarios")

@login_required
def cambiar_estado_usuario(request, pk):
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para realizar esta acción")
        return redirect("dashboard")
    
    try:
        usuario = Usuario.objects.get(pk=pk)
        
        # No permitir cambiar el estado del usuario actual
        if usuario == request.user:
            messages.error(request, "No puedes cambiar tu propio estado")
            return redirect("listar_usuarios")
        
        # Cambiar estado
        usuario.is_active = not usuario.is_active
        usuario.save()
        
        estado = "activado" if usuario.is_active else "desactivado"
        messages.success(request, f"Usuario '{usuario.username}' {estado} exitosamente")
        
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe")
    
    return redirect("listar_usuarios")

@login_required
def eliminar_usuario(request, pk):
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para realizar esta acción")
        return redirect("dashboard")
    
    try:
        usuario = Usuario.objects.get(pk=pk)
        # No permitir que se elimine a sí mismo
        if usuario == request.user:
            messages.error(request, "No puedes eliminar tu propio usuario")
            return redirect("listar_usuarios")
        
        username = usuario.username
        usuario.delete()
        messages.success(request, f"Usuario '{username}' eliminado exitosamente")
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe")
    
    return redirect("listar_usuarios")

