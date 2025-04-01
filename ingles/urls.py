from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cursos/', include('cursos.urls')),  # Incluyendo las URLs de la aplicación "cursos"
    path('usuarios/', include('usuarios.urls')),
    path('actividades/', include('actividades.urls')),
    path('inscripciones/', include('inscripciones.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)