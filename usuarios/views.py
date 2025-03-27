from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.views import View
from django.views.generic import UpdateView 
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from .models import Usuario
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .forms import PerfilForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
)
from cursos.models import Curso


# =================== Cambio de Contraseña ===================
@method_decorator(login_required, name="dispatch")
class CambioPasswordView(View):
    """ Vista para cambiar la contraseña del usuario """
    
    def get(self, request):
        form = SetPasswordForm(user=request.user)  
        return render(request, "usuarios/cambio_password.html", {"form": form})

    def post(self, request):
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.cambiar_password(form.cleaned_data["new_password1"])  # Método en Usuario
            messages.success(request, "Contraseña cambiada exitosamente")
            return redirect("usuarios:perfil")
        
        return render(request, "usuarios/cambio_password.html", {"form": form})


# =================== Autenticación ===================
class RegistroView(View):
    """ Vista para el registro de usuarios """
    
    def get(self, request):
        form = RegistroForm()
        return render(request, "usuarios/registro.html", {"form": form})

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.guardar_usuario(form.cleaned_data["password1"])  # Método en Usuario
            login(request, usuario)
            return redirect("usuarios:perfil")
        return render(request, "usuarios/registro.html", {"form": form})


class LoginView(DjangoLoginView):
    """ Vista para el inicio de sesión """
    template_name = "usuarios/login.html"
    authentication_form = LoginForm  # Usamos el formulario personalizado

    def form_valid(self, form):
        """ Redirige al perfil tras un login exitoso """
        login(self.request, form.get_user())
        return redirect("usuarios:perfil")



class LogoutView(View):
    """ Vista para cerrar sesión """
    
    def get(self, request):
        logout(request)  # Cierra la sesión del usuario
        return redirect("usuarios:login")  # Redirige al login


class PerfilView(View):
    """ Vista para mostrar el perfil del usuario """

    def get(self, request):
        # Obtiene todos los cursos del usuario
        cursos = Curso.objects.filter(profesor=request.user)  # Devuelve una lista de cursos

        # Si no hay cursos, muestra un mensaje de advertencia
        if not cursos.exists():
            messages.warning(request, "No tienes ningún curso disponible.")
        
        return render(request, "usuarios/perfil.html", {"cursos": cursos})


class EditarPerfilView(UpdateView):
    """Vista para modificar el perfil del usuario"""
    model = Usuario
    form_class = PerfilForm
    template_name = "usuarios/editar_perfil.html"

    def get_object(self):
        return self.request.user  # El usuario actual

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("usuarios:perfil")  # Redirige de nuevo al perfil

# =================== Restablecimiento de Contraseña ===================
class RestablecerPasswordView(PasswordResetView):
    """ Vista para solicitar restablecimiento de contraseña """
    template_name = "usuarios/restablecer_password.html"
    success_url = reverse_lazy("usuarios:password_reset_done")
    email_template_name = "usuarios/email_password_reset.html"
    form_class = PasswordResetForm


class RestablecerPasswordConfirmView(PasswordResetConfirmView):
    """ Vista para confirmar nueva contraseña """
    template_name = "usuarios/restablecer_password_confirm.html"
    success_url = reverse_lazy("usuarios:password_reset_complete")
    form_class = SetPasswordForm


class RestablecerPasswordMensajeView(View):
    """ Vista genérica para mostrar mensajes después del restablecimiento """
    
    def get(self, request, mensaje):
        mensajes = {
            "enviado": "Si el correo ingresado es correcto, recibirás instrucciones para restablecer tu contraseña.",
            "completo": "Tu contraseña ha sido restablecida exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.",
        }
        return render(request, "usuarios/restablecer_password_mensaje.html", {"mensaje": mensajes.get(mensaje, "")})
