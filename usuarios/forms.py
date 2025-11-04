from django import forms
from .models import Usuario

# ==================== FORMULARIO DE USUARIO ====================

class UsuarioForm(forms.ModelForm):
    """
    Formulario para crear y editar usuarios del sistema.
    
    Este formulario extiende ModelForm para generar automáticamente campos
    basándose en el modelo Usuario. Agrega campos adicionales para contraseña
    y su confirmación, con validaciones personalizadas.
    
    CAMPOS DEL FORMULARIO:
    - username: Nombre de usuario único
    - first_name: Nombre
    - last_name: Apellido
    - email: Correo electrónico
    - rol: Rol del usuario (admin/técnico)
    - password: Contraseña (campo adicional, no del modelo)
    - password_confirm: Confirmación de contraseña (campo adicional)
    
    VALIDACIONES:
    - Las contraseñas deben coincidir
    - Username debe ser único
    - Email debe tener formato válido
    
    USO:
        # Crear usuario
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()  # Hashea la contraseña automáticamente
        
        # Editar usuario
        form = UsuarioForm(request.POST, instance=usuario)
    """
    
    # Campo de contraseña con widget PasswordInput (oculta los caracteres)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',       # Clase Bootstrap
            'placeholder': 'Contraseña'    # Texto de ayuda
        }),
        label='Contraseña'
    )
    
    # Campo de confirmación de contraseña
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        }),
        label='Confirmar contraseña'
    )

    class Meta:
        # Modelo asociado al formulario
        model = Usuario
        
        # Campos del modelo a incluir en el formulario
        # password y password_confirm se agregan manualmente arriba
        fields = ['username', 'first_name', 'last_name', 'email', 'rol']
        
        # Widgets personalizados con estilos Bootstrap
        widgets = {
            # Campo de texto para username
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            # Campo de texto para nombre
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            # Campo de texto para apellido
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            # Campo de email con validación HTML5
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            # Selector desplegable para el rol
            'rol': forms.Select(attrs={
                'class': 'form-select'  # Clase Bootstrap para select
            })
        }
        
        # Etiquetas personalizadas para cada campo
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'rol': 'Rol de usuario'
        }

    def clean(self):
        """
        Validación personalizada del formulario completo.
        
        Verifica que las contraseñas coincidan antes de procesar el formulario.
        Esta validación se ejecuta después de las validaciones individuales
        de cada campo.
        
        Returns:
            dict: Datos limpios y validados del formulario
            
        Raises:
            ValidationError: Si las contraseñas no coinciden
        """
        # Obtener datos ya validados individualmente
        cleaned_data = super().clean()
        
        # Extraer contraseñas del formulario
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Validar que ambas contraseñas existan y coincidan
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden')
        
        return cleaned_data

    def save(self, commit=True):
        """
        Guarda el usuario con la contraseña hasheada.
        
        Sobrescribe el método save para hashear la contraseña antes de
        guardarla en la base de datos. Django nunca debe guardar contraseñas
        en texto plano.
        
        Args:
            commit (bool): Si True, guarda inmediatamente en la BD.
                          Si False, retorna instancia sin guardar.
        
        Returns:
            Usuario: Instancia del usuario creado/actualizado
        """
        # Crear instancia del usuario sin guardar aún
        user = super().save(commit=False)
        
        # Hashear la contraseña usando el método de Django
        # set_password convierte la contraseña en un hash seguro
        user.set_password(self.cleaned_data['password'])
        
        # Guardar en la base de datos si commit=True
        if commit:
            user.save()
        
        return user
