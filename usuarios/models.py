from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(AbstractUser):
    ROLES = [
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante')
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default='estudiante', blank=False, null=False)
    imagen_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)  # Nueva imagen de perfil

    def __str__(self):
        return self.username

    def guardar_usuario(self, commit=True):
        """Guarda el usuario encriptando la contraseña si aún no está encriptada."""
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        if commit:
            self.save()

    def cambiar_password(self, nueva_password):
        """Cambia la contraseña del usuario de manera segura"""
        self.set_password(nueva_password)
        self.save()
