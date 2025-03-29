from django import forms
from .models import Curso, Leccion

class CursoForm(forms.ModelForm):
    """Formulario para crear y editar un curso con mejoras visuales"""
    
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del curso'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del curso'}),
        }


class LeccionForm(forms.ModelForm):
    """Formulario para crear y editar una lección con mejoras visuales"""
    
    class Meta:
        model = Leccion
        fields = ['titulo', 'contenido', 'orden', 'imagen', 'video']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la lección'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Contenido de la lección'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



########################################################################

