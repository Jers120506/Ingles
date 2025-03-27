from django.urls import path
from .views import (
    LoginView, RegistroView, PerfilView, LogoutView,
    CambioPasswordView, RestablecerPasswordView,EditarPerfilView
)

from .views import (
    RestablecerPasswordConfirmView,
    RestablecerPasswordMensajeView,
)

app_name = "usuarios"  # Para usar reverse("usuarios:login"), etc.

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registro/", RegistroView.as_view(), name="registro"),
    path("perfil/", PerfilView.as_view(), name="perfil"),
    path('perfil/editar/', EditarPerfilView.as_view(), name='editar_perfil'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("cambio-password/", CambioPasswordView.as_view(), name="cambio_password"),
    path("restablecer-password/", RestablecerPasswordView.as_view(), name="restablecer_password"),
    path("restablecer-password/enviado/", RestablecerPasswordMensajeView.as_view(), {"mensaje": "enviado"}, name="password_reset_done"),
    path("restablecer-password/confirmar/<uidb64>/<token>/", RestablecerPasswordConfirmView.as_view(), name="password_reset_confirm"),
    path("restablecer-password/completo/", RestablecerPasswordMensajeView.as_view(), {"mensaje": "completo"}, name="password_reset_complete"),
]
