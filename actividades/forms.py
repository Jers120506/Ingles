from django import forms
from django.forms import inlineformset_factory
from .models import Evaluacion, PreguntaOpcionMultiple, OpcionRespuesta

# Formulario para Evaluaciones
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['titulo', 'descripcion', 'tipo_actividad']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la evaluación'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción (opcional)', 'rows': 3}),
            'tipo_actividad': forms.Select(attrs={'class': 'form-control'})
        }

# Formulario para Preguntas de Opción Múltiple
class PreguntaOpcionMultipleForm(forms.ModelForm):
    class Meta:
        model = PreguntaOpcionMultiple
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe la pregunta aquí', 'rows': 2})
        }

# Formulario para Opciones de Respuesta
class OpcionRespuestaForm(forms.ModelForm):
    class Meta:
        model = OpcionRespuesta
        fields = ['texto', 'es_correcta']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto de la opción'}),
            'es_correcta': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

# Formset para gestionar múltiples preguntas dentro de una evaluación
PreguntaFormset = inlineformset_factory(
    Evaluacion, PreguntaOpcionMultiple,
    form=PreguntaOpcionMultipleForm,
    extra=1, can_delete=True
)

# Formset para gestionar múltiples opciones dentro de una pregunta
OpcionFormset = inlineformset_factory(
    PreguntaOpcionMultiple, OpcionRespuesta,
    form=OpcionRespuestaForm,
    extra=4, can_delete=True
)
