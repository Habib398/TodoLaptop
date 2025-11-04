"""
Vistas del módulo de usuarios.

Este módulo maneja toda la lógica de autenticación y gestión de usuarios:
- Inicio y cierre de sesión
- Dashboard principal
- CRUD completo de usuarios (solo para administradores)
- Cambio de estado de usuarios (activar/desactivar)

CONTROL DE ACCESO:
- login_view: Acceso público
- logout_view: Acceso público
- dashboard: Requiere autenticación
- Gestión de usuarios: Solo administradores (rol='admin')
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioForm
from .models import Usuario

# ==================== AUTENTICACIÓN ====================

def login_view(request):
    """
    Vista de inicio de sesión.
    
    Maneja el proceso de autenticación de usuarios. Si las credenciales
    son correctas, redirige al dashboard. Si son incorrectas, muestra
    un mensaje de error.
    
    FLUJO:
    1. Si GET: Muestra formulario de login
    2. Si POST: Valida credenciales
       - Éxito: Inicia sesión y redirige a dashboard
       - Fallo: Muestra mensaje de error
    
    Args:
        request: Objeto HttpRequest
        
    Returns:
        HttpResponse: Página de login o redirección al dashboard
    """
    if request.method == "POST":
        # Obtener credenciales del formulario
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Registros de depuración para troubleshooting
        print(f"[DEBUG] Login attempt - Username: {username}")
        print(f"[DEBUG] Request method: {request.method}")
        print(f"[DEBUG] Request origin: {request.headers.get('origin', 'No origin')}")
        
        # Autenticar usuario contra la base de datos
        # authenticate() verifica username/password y devuelve User si es válido
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Credenciales válidas: iniciar sesión
            login(request, user)  # Crea la sesión del usuario
            print(f"[DEBUG] Login successful for user: {username}")
            return redirect("dashboard")  # Redirigir a página principal
        else:
            # Credenciales inválidas: mostrar error
            print(f"[DEBUG] Login failed for user: {username}")
            messages.error(request, "Usuario o contraseña incorrectos")
    
    # Mostrar formulario de login (GET o POST fallido)
    # Mostrar formulario de login (GET o POST fallido)
    return render(request, "usuarios/login.html")

def logout_view(request):
    """
    Vista de cierre de sesión.
    
    Cierra la sesión actual del usuario y lo redirige a la página de login.
    Limpia todos los datos de sesión del usuario.
    
    Args:
        request: Objeto HttpRequest
        
    Returns:
        HttpResponseRedirect: Redirige a la página de login
    """
    # Cerrar sesión del usuario actual
    logout(request)
    # Redirigir al login
    return redirect("login")

# ==================== DASHBOARD ====================

@login_required
def dashboard(request):
    """
    Vista del dashboard principal.
    
    Página de inicio después del login. Muestra diferentes opciones
    según el rol del usuario (administrador o técnico).
    
    DECORADOR:
    - @login_required: Solo usuarios autenticados pueden acceder
    
    Args:
        request: Objeto HttpRequest con el usuario autenticado
        
    Returns:
        HttpResponse: Renderiza el template del dashboard
    """
    return render(request, "usuarios/dashboard.html")

# ==================== GESTIÓN DE USUARIOS (SOLO ADMIN) ====================

@login_required
def agregar_usuario(request):
    """
    Vista para crear un nuevo usuario (solo administradores).
    
    Permite a los administradores crear nuevos usuarios del sistema.
    Valida que las contraseñas coincidan y que el username sea único.
    
    PERMISOS:
    - Solo usuarios con rol='admin' pueden acceder
    - Redirige al dashboard si el usuario no es admin
    
    VALIDACIONES:
    - Contraseñas deben coincidir
    - Username debe ser único
    
    Args:
        request: Objeto HttpRequest con datos POST del formulario
        
    Returns:
        HttpResponseRedirect: Redirige a la lista de usuarios
    """
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para acceder a esta página")
        return redirect("dashboard")
    
    if request.method == "POST":
        # Obtener datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        rol = request.POST.get('rol')
        
        # Validación: las contraseñas deben coincidir
        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("listar_usuarios")
        
        # Validación: el username debe ser único
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, f"El usuario '{username}' ya existe")
            return redirect("listar_usuarios")
        
        # Crear usuario usando create_user() para hashear la contraseña
        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,  # Se hasheará automáticamente
            rol=rol
        )
        messages.success(request, f"Usuario '{username}' creado exitosamente")
        return redirect("listar_usuarios")
    
    # Si no es POST, redirigir a la lista
    return redirect("listar_usuarios")

@login_required
def listar_usuarios(request):
    """
    Vista para listar todos los usuarios del sistema (solo administradores).
    
    Muestra una tabla con todos los usuarios registrados. Incluye funcionalidad
    de búsqueda por username, nombre o apellido.
    
    PERMISOS:
    - Solo usuarios con rol='admin' pueden acceder
    
    BÚSQUEDA:
    - Parámetro GET 'buscar': filtra usuarios por username, first_name o last_name
    - Búsqueda insensible a mayúsculas/minúsculas (__icontains)
    - Ordenados por fecha de creación descendente (más recientes primero)
    
    Args:
        request: Objeto HttpRequest con parámetro GET opcional 'buscar'
        
    Returns:
        HttpResponse: Renderiza template con lista de usuarios y término de búsqueda
    """
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para acceder a esta página")
        return redirect("dashboard")
    
    # Obtener término de búsqueda del querystring
    buscar = request.GET.get('buscar', '')
    
    if buscar:
        # Buscar en múltiples campos usando operador OR (|)
        # __icontains: contiene el texto (case-insensitive)
        usuarios = Usuario.objects.filter(
            username__icontains=buscar
        ).order_by('-date_joined') | Usuario.objects.filter(
            first_name__icontains=buscar
        ).order_by('-date_joined') | Usuario.objects.filter(
            last_name__icontains=buscar
        ).order_by('-date_joined')
    else:
        # Sin búsqueda: mostrar todos los usuarios
        usuarios = Usuario.objects.all().order_by('-date_joined')
    
    # Renderizar template con lista de usuarios y término de búsqueda
    return render(request, "usuarios/listar_usuarios.html", {
        "usuarios": usuarios,
        "buscar": buscar  # Para mantener el valor en el input de búsqueda
    })

@login_required
def editar_usuario(request, pk):
    """
    Vista para editar un usuario existente (solo administradores).
    
    Permite modificar los datos de un usuario: username, email, nombre,
    apellido, rol y opcionalmente la contraseña.
    
    PERMISOS:
    - Solo usuarios con rol='admin' pueden acceder
    
    VALIDACIONES:
    - Username debe ser único (excepto el del usuario actual)
    - Si se cambia contraseña, debe confirmarla
    
    NOTAS:
    - Si no se proporciona nueva contraseña, mantiene la actual
    - La contraseña se hashea automáticamente con set_password()
    
    Args:
        request: Objeto HttpRequest con datos POST del formulario
        pk (int): ID (primary key) del usuario a editar
        
    Returns:
        HttpResponseRedirect: Redirige a la lista de usuarios
    """
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para realizar esta acción")
        return redirect("dashboard")
    
    try:
        # Obtener usuario por ID
        usuario = Usuario.objects.get(pk=pk)
        
        if request.method == "POST":
            # Obtener datos del formulario
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            rol = request.POST.get('rol')
            new_password = request.POST.get('new_password')
            new_password_confirm = request.POST.get('new_password_confirm')
            
            # Validar que el username no esté en uso por otro usuario
            # exclude(pk=pk): excluir el usuario actual de la búsqueda
            if Usuario.objects.filter(username=username).exclude(pk=pk).exists():
                messages.error(request, f"El usuario '{username}' ya está en uso")
                return redirect("listar_usuarios")
            
            # Actualizar datos básicos del usuario
            usuario.username = username
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.rol = rol
            
            # Cambiar contraseña solo si se proporcionó una nueva
            if new_password:
                # Validar que las contraseñas coincidan
                if new_password != new_password_confirm:
                    messages.error(request, "Las contraseñas no coinciden")
                    return redirect("listar_usuarios")
                # Hashear y guardar nueva contraseña
                usuario.set_password(new_password)
            
            # Guardar cambios en la base de datos
            usuario.save()
            messages.success(request, f"Usuario '{username}' actualizado exitosamente")
            return redirect("listar_usuarios")
            
    except Usuario.DoesNotExist:
        # Usuario no encontrado en la BD
        messages.error(request, "El usuario no existe")
    
    return redirect("listar_usuarios")

@login_required
def cambiar_estado_usuario(request, pk):
    """
    Vista para activar/desactivar un usuario (solo administradores).
    
    Alterna el estado activo del usuario (is_active). Los usuarios inactivos
    no pueden iniciar sesión en el sistema.
    
    PERMISOS:
    - Solo usuarios con rol='admin' pueden acceder
    
    RESTRICCIONES:
    - Un administrador no puede cambiar su propio estado
    
    ESTADOS:
    - is_active=True: Usuario puede iniciar sesión
    - is_active=False: Usuario bloqueado, no puede iniciar sesión
    
    Args:
        request: Objeto HttpRequest
        pk (int): ID (primary key) del usuario a cambiar estado
        
    Returns:
        HttpResponseRedirect: Redirige a la lista de usuarios
    """
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para realizar esta acción")
        return redirect("dashboard")
    
    try:
        # Obtener usuario por ID
        usuario = Usuario.objects.get(pk=pk)
        
        # No permitir cambiar el estado del usuario actual
        # Previene que el admin se bloquee a sí mismo
        if usuario == request.user:
            messages.error(request, "No puedes cambiar tu propio estado")
            return redirect("listar_usuarios")
        
        # Alternar estado activo
        usuario.is_active = not usuario.is_active
        usuario.save()
        
        # Mensaje descriptivo según el nuevo estado
        estado = "activado" if usuario.is_active else "desactivado"
        messages.success(request, f"Usuario '{usuario.username}' {estado} exitosamente")
        
    except Usuario.DoesNotExist:
        # Usuario no encontrado en la BD
        messages.error(request, "El usuario no existe")
    
    return redirect("listar_usuarios")

@login_required
def eliminar_usuario(request, pk):
    """
    Vista para eliminar un usuario del sistema (solo administradores).
    
    Elimina permanentemente un usuario de la base de datos. Esta acción
    no se puede deshacer.
    
    PERMISOS:
    - Solo usuarios con rol='admin' pueden acceder
    
    RESTRICCIONES:
    - Un administrador no puede eliminarse a sí mismo
    
    CONSIDERACIONES:
    - Esta es una eliminación física (DELETE en la BD)
    - Se pierden todos los datos asociados al usuario
    - Alternativa: usar cambiar_estado_usuario() para desactivar
    
    Args:
        request: Objeto HttpRequest
        pk (int): ID (primary key) del usuario a eliminar
        
    Returns:
        HttpResponseRedirect: Redirige a la lista de usuarios
    """
    # Verificar que el usuario actual sea administrador
    if request.user.rol != 'admin':
        messages.error(request, "No tienes permisos para realizar esta acción")
        return redirect("dashboard")
    
    try:
        # Obtener usuario por ID
        usuario = Usuario.objects.get(pk=pk)
        
        # No permitir que se elimine a sí mismo
        # Previene que el admin se elimine accidentalmente
        if usuario == request.user:
            messages.error(request, "No puedes eliminar tu propio usuario")
            return redirect("listar_usuarios")
        
        # Guardar username para el mensaje de confirmación
        username = usuario.username
        
        # Eliminar usuario de la base de datos
        usuario.delete()
        
        messages.success(request, f"Usuario '{username}' eliminado exitosamente")
        
    except Usuario.DoesNotExist:
        # Usuario no encontrado en la BD
        messages.error(request, "El usuario no existe")
    
    return redirect("listar_usuarios")

