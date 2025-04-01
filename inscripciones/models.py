from django.db import models
from django.conf import settings
from usuarios.models import Usuario
from cursos.models import Curso

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="inscripciones")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="inscripciones")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)