from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
import re
from cursos.models import Leccion
from django.contrib import messages
from .models import Evaluacion, PreguntaOpcionMultiple, OpcionRespuesta, Leccion, PreguntaCompletarFrase, RespuestaCompletarFrase

def crear_actividad(request, leccion_id, tipo):
    """Vista para la creación de nuevas actividades sin Django Forms ni Formsets."""
    leccion = get_object_or_404(Leccion, id=leccion_id)

    if tipo == "completar_frases":
        return crear_completar_frases(request, leccion_id)

    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()

        # Validar campos básicos
        if not titulo:
            messages.error(request, "El título no puede estar vacío.")
        else:
            # Crear una nueva evaluación sin reutilizar una existente
            evaluacion = Evaluacion.objects.create(
                leccion=leccion,
                tipo_actividad=tipo,
                creado_por=request.user,
                titulo=titulo,
                descripcion=descripcion
            )

            # Procesar preguntas y opciones
            preguntas_validas = True
            num_preguntas = int(request.POST.get("num_preguntas", 0))

            for i in range(num_preguntas):
                texto_pregunta = request.POST.get(f"pregunta_{i}", "").strip()
                if not texto_pregunta:
                    continue  # Ignorar preguntas vacías

                pregunta = PreguntaOpcionMultiple.objects.create(
                    evaluacion=evaluacion,
                    texto=texto_pregunta
                )

                # Agregar opciones de respuesta
                num_opciones = int(request.POST.get(f"num_opciones_{i}", 0))
                tiene_respuesta_correcta = False

                for j in range(num_opciones):
                    texto_opcion = request.POST.get(f"opcion_{i}_{j}", "").strip()
                    es_correcta = request.POST.get(f"correcta_{i}_{j}") == "on"

                    if texto_opcion:
                        OpcionRespuesta.objects.create(
                            pregunta=pregunta,
                            texto=texto_opcion,
                            es_correcta=es_correcta
                        )
                        if es_correcta:
                            tiene_respuesta_correcta = True

                if not tiene_respuesta_correcta:
                    preguntas_validas = False
                    messages.error(request, f"La pregunta '{texto_pregunta}' debe tener al menos una respuesta correcta.")

            if preguntas_validas:
                messages.success(request, "Evaluación creada correctamente.")
                return redirect("cursos:detalle_leccion", pk=leccion_id)
            else:
                messages.error(request, "Corrige los errores en las preguntas.")

    return render(request, "actividades/crear_actividad.html", {
        "leccion": leccion
    })

def eliminar_actividad(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)

    # Verificar si el usuario es profesor y creador de la evaluación
    if request.user.rol != "profesor" or request.user != evaluacion.creado_por:
        messages.error(request, "No tienes permiso para eliminar esta evaluación.")
        return redirect('cursos:detalle_curso', evaluacion.leccion.curso.pk)

    # Obtener la lección antes de eliminar la evaluación
    leccion = evaluacion.leccion
    evaluacion.delete()
    messages.success(request, "Evaluación eliminada correctamente.")

    return redirect('cursos:detalle_leccion', leccion.pk)


class DetalleEvaluacionView(DetailView):
    model = Evaluacion
    template_name = "actividades/detalle_evaluacion.html"
    context_object_name = "evaluacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["preguntas_opcion_multiple"] = PreguntaOpcionMultiple.objects.filter(evaluacion=self.object)
        context["preguntas_completar_frase"] = PreguntaCompletarFrase.objects.filter(evaluacion=self.object)
        return context

    

###########################################

def crear_completar_frases(request, leccion_id):
    """Vista para crear una actividad de completar frases en una lección específica."""
    leccion = get_object_or_404(Leccion, id=leccion_id)

    if request.method == "POST":
        print(request.POST)  # 🔍 Verifica los datos recibidos

        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion", "")
        preguntas = request.POST.getlist("preguntas[]")  # Corrección
        respuestas = request.POST.getlist("respuestas[]")  # Corrección

        if not titulo or not preguntas:
            messages.error(request, "Debes completar todos los campos obligatorios.")
            return render(request, "actividades/crear_completar_frases.html", {"leccion": leccion})

        # Crear la evaluación
        evaluacion = Evaluacion.objects.create(
            leccion=leccion,
            titulo=titulo,
            descripcion=descripcion,
            tipo_actividad="completar_frases",
            creado_por=request.user,
        )

        # Procesar preguntas y respuestas
        for i, texto_pregunta in enumerate(preguntas):
            texto_pregunta = texto_pregunta.strip()
            espacios = [m.start() for m in re.finditer(r'\[\.\.\.\]', texto_pregunta)]

            if not espacios:
                messages.error(request, f"La pregunta '{texto_pregunta}' no contiene ningún espacio '[...]'.")
                return render(request, "actividades/crear_completar_frases.html", {"leccion": leccion})

            pregunta = PreguntaCompletarFrase.objects.create(
                evaluacion=evaluacion,
                texto=texto_pregunta
            )

            respuestas_pregunta = respuestas[i].split(";")  # Separa respuestas por ";"

            if len(respuestas_pregunta) != len(espacios):
                messages.error(request, f"La pregunta '{texto_pregunta}' no tiene el mismo número de respuestas que espacios '[...]'.")
                return render(request, "actividades/crear_completar_frases.html", {"leccion": leccion})

            # Guardar respuestas con su respectiva posición
            for j, respuesta in enumerate(respuestas_pregunta):
                partes = [r.strip() for r in respuesta.split(",")]  # Separa alternativas por ","
                respuesta_correcta = partes[0]
                alternativas = ",".join(partes[1:]) if len(partes) > 1 else ""

                RespuestaCompletarFrase.objects.create(
                    pregunta=pregunta,
                    posicion=j,
                    respuesta_correcta=respuesta_correcta,
                    alternativas=alternativas
                )

        messages.success(request, "Actividad de completar frases creada exitosamente.")
        return redirect("cursos:detalle_leccion", pk=leccion.id)


    return render(request, "actividades/crear_completar_frases.html", {"leccion": leccion})

##############################################################

def resolver_actividad(request, evaluacion_id):
    """Vista para que el alumno resuelva una actividad."""
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)

    # Verificar si el usuario es estudiante
    if request.user.rol != 'estudiante':
        messages.error(request, "Solo los estudiantes pueden resolver esta actividad.")
        return redirect("cursos:detalle_leccion", pk=evaluacion.leccion.pk)

    # Obtener las preguntas según el tipo de evaluación
    if evaluacion.tipo_actividad == "opcion_multiple":
        preguntas = PreguntaOpcionMultiple.objects.filter(evaluacion=evaluacion)
    elif evaluacion.tipo_actividad == "completar_frases":
        preguntas = PreguntaCompletarFrase.objects.filter(evaluacion=evaluacion)
    else:
        messages.error(request, "Tipo de actividad no válido.")
        return redirect("cursos:detalle_leccion", pk=evaluacion.leccion.pk)

    if request.method == "POST":
        puntaje = 0
        total_preguntas = len(preguntas)

        if evaluacion.tipo_actividad == "opcion_multiple":
            for pregunta in preguntas:
                respuesta_seleccionada_id = request.POST.get(f"pregunta_{pregunta.id}")
                if respuesta_seleccionada_id:
                    opcion_seleccionada = OpcionRespuesta.objects.get(id=respuesta_seleccionada_id)
                    if opcion_seleccionada.es_correcta:
                        puntaje += 1

        elif evaluacion.tipo_actividad == "completar_frases":
            for pregunta in preguntas:
                respuestas_correctas = list(RespuestaCompletarFrase.objects.filter(pregunta=pregunta))
                respuestas_usuario = request.POST.getlist(f"pregunta_{pregunta.id}")

                if len(respuestas_usuario) == len(respuestas_correctas):
                    correctas = sum(
                        1 for i in range(len(respuestas_correctas))
                        if respuestas_usuario[i].strip().lower() == respuestas_correctas[i].respuesta_correcta.lower()
                    )
                    if correctas == len(respuestas_correctas):
                        puntaje += 1

        messages.success(request, f"Has completado la actividad. Tu puntaje es {puntaje}/{total_preguntas}.")
        return render(request, 'actividades/resolver_actividad.html', {
            'evaluacion': evaluacion,
            'preguntas': preguntas,
            'puntaje': puntaje,
            'total_preguntas': total_preguntas
        })

    return render(request, "actividades/resolver_actividad.html", {
        "evaluacion": evaluacion,
        "preguntas": preguntas
    })

