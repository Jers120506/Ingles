from django.urls import path
from .views import crear_actividad
from .views import DetalleEvaluacionView,eliminar_actividad,crear_completar_frases,resolver_actividad

app_name = 'actividades'
urlpatterns = [
    path('leccion/<int:leccion_id>/actividad/<str:tipo>/', crear_actividad, name='crear_actividad'),
    path('evaluacion/<int:pk>/', DetalleEvaluacionView.as_view(), name='detalle_evaluacion'),
    path('eliminar/<int:evaluacion_id>/', eliminar_actividad, name='eliminar_actividad'),
    path('crear/<int:leccion_id>/completar_frases/', crear_completar_frases, name='crear_completar_frases'),
    path('resolver/<int:evaluacion_id>/', resolver_actividad, name='resolver_actividad')
]


