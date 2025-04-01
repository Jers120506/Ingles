# usuarios/decoradores.py
from django.http import HttpResponseForbidden
from functools import wraps

def solo_profesor(view_func):
    """Decorador para verificar si el usuario es un profesor."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.rol != 'profesor':
            return HttpResponseForbidden("No tienes permisos para acceder a esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
