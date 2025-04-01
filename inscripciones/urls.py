# inscripciones/urls.py
from django.urls import path
from .views import InscribirseCursoView
from django.conf import settings
from django.conf.urls.static import static
app_name = "inscripciones"
urlpatterns = [
    path("inscripciones/<int:curso_id>/inscribirse/", InscribirseCursoView.as_view(), name="inscribirse_curso"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)