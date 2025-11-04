from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    """
    Formulario para crear y editar productos del inventario.
    
    Este formulario utiliza ModelForm para generar automáticamente los campos
    basándose en el modelo Producto. Incluye validaciones y widgets personalizados
    con estilos Bootstrap para mejorar la experiencia del usuario.
    """
    
    class Meta:
        # Modelo asociado al formulario
        model = Producto
        
        # Campos que se mostrarán en el formulario
        fields = ['nombre', 'descripcion', 'precio', 'cantidad_stock']
        
        # Etiquetas personalizadas para cada campo
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'cantidad_stock': 'Cantidad en stock'
        }
        
        # Widgets personalizados con estilos y validaciones HTML5
        widgets = {
            # Campo de texto para el nombre del producto
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Laptop Dell Inspiron'
            }),
            # Área de texto para la descripción (4 filas)
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción breve del producto'
            }),
            # Campo numérico para precio con validación de decimales
            # step='0.01' permite ingresar centavos
            # min='0' evita precios negativos
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            # Campo numérico para cantidad en stock
            # min='0' evita cantidades negativas
            'cantidad_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Cantidad disponible'
            }),
        }
