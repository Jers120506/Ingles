from django.db import models
from django.conf import settings

from cursos.models import Leccion  # Importamos el modelo de Lección

# Modelo para almacenar las evaluaciones dentro de una lección
class Evaluacion(models.Model):
    TIPO_ACTIVIDAD = [
        ('opciones_multiples', 'Opciones Múltiples'),
        ('completar_frases', 'Completar Frases'),
        ('arrastrar_soltar', 'Arrastrar y Soltar'),
        ('pronunciacion', 'Pronunciación'),
        ('traduccion', 'Traducción'),
    ]
    
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name="evaluaciones")
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    tipo_actividad = models.CharField(max_length=50, choices=TIPO_ACTIVIDAD)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_actividad_display()}"

# Modelo para las preguntas de opción múltiple
class PreguntaOpcionMultiple(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name="preguntas")
    texto = models.TextField()

    def __str__(self):
        return self.texto

# Modelo para las opciones de respuesta de opción múltiple
class OpcionRespuesta(models.Model):
    pregunta = models.ForeignKey(PreguntaOpcionMultiple, on_delete=models.CASCADE, related_name="opciones")
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} {'(Correcta)' if self.es_correcta else ''}"


##############################################################################33
import re

class PreguntaCompletarFrase(models.Model):
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name="preguntas_completar_frase")
    texto = models.TextField(help_text="Usa '[...]' para indicar los espacios a completar.")

    def obtener_espacios(self):
        """Devuelve una lista con los espacios a completar en la frase."""
        return [m.start() for m in re.finditer(r'\[\.\.\.\]', self.texto)]

    def __str__(self):
        return self.texto


class RespuestaCompletarFrase(models.Model):
    pregunta = models.ForeignKey(PreguntaCompletarFrase, on_delete=models.CASCADE, related_name="respuestas")
    posicion = models.PositiveIntegerField(help_text="Posición del espacio en la oración (orden).")
    respuesta_correcta = models.CharField(max_length=255)
    alternativas = models.TextField(blank=True, help_text="Sinónimos separados por comas (opcional).")

    def obtener_alternativas(self):
        """Devuelve una lista de alternativas correctas, ignorando mayúsculas y tildes."""
        return [self.respuesta_correcta.lower()] + [alt.strip().lower() for alt in self.alternativas.split(",") if alt.strip()]

    def __str__(self):
        return f"{self.pregunta} - {self.respuesta_correcta}"
