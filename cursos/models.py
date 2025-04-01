from django.db import models
from django.conf import settings

class Curso(models.Model):
    """Modelo para representar un curso"""
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'rol': 'profesor'}
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def cambiar_estado_publicacion(self, estado):
        """Método para publicar o despublicar un curso"""
        self.publicado = estado
        self.save()

    @classmethod
    def obtener_publicados(cls):
        """Obtener todos los cursos publicados"""
        return cls.objects.filter(publicado=True)

class Leccion(models.Model):
    """Modelo para representar una lección dentro de un curso"""
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="lecciones")
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    orden = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to="lecciones/imagenes/", blank=True, null=True)
    video = models.FileField(upload_to="lecciones/videos/", blank=True, null=True)
   


    def __str__(self):
        return f"{self.orden}. {self.titulo} - {self.curso.nombre}"

    def cambiar_orden(self, nuevo_orden):
        """Método para cambiar el orden de la lección dentro del curso"""
        self.orden = nuevo_orden
        self.save()

    class Meta:
        ordering = ["orden"]  # Ordenar lecciones por su número


####################################################################################

