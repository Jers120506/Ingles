from django.urls import path
from .views import (
    MisCursosView, DetalleCursoView, SeleccionarCursoView,
    CrearLeccionView, EditarLeccionView, CrearCursoView, EditarCursoView,EliminarCursoView,DetalleLeccionView,VerCursosView
    
)
from django.conf import settings
from django.conf.urls.static import static
app_name = "cursos"

urlpatterns = [
    path("mis-cursos/", MisCursosView.as_view(), name="mis_cursos"),
    path("curso/<int:pk>/", DetalleCursoView.as_view(), name="detalle_curso"),
    path("ver-cursos/", VerCursosView.as_view(), name="ver_cursos"),
    path("curso/crear/", CrearCursoView.as_view(), name="crear_curso"),
    path("curso/editar/<int:pk>/", EditarCursoView.as_view(), name="editar_curso"),
    path("curso/<int:curso_id>/crear-leccion/", CrearLeccionView.as_view(), name="crear_leccion"),
    path("curso/<int:curso_id>/editar-leccion/<int:pk>/", EditarLeccionView.as_view(), name="editar_leccion"),
    path("seleccionar-curso/", SeleccionarCursoView.as_view(), name="seleccionar_curso"),
    path("curso/eliminar/<int:pk>/", EliminarCursoView.as_view(), name="eliminar_curso"),
    path('leccion/<int:pk>/', DetalleLeccionView.as_view(), name='detalle_leccion'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
