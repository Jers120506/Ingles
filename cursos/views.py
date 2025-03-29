from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Curso, Leccion
from .forms import CursoForm, LeccionForm
from django.views.generic import DeleteView
from inscripciones.models import Inscripcion


from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from actividades.models import Evaluacion, PreguntaOpcionMultiple, OpcionRespuesta
from actividades.forms import PreguntaOpcionMultipleForm, OpcionRespuestaForm
from cursos.models import Leccion

class EsProfesorMixin(UserPassesTestMixin):
    """Mixin para validar que el usuario es un profesor."""
    def test_func(self):
        return self.request.user.rol == "profesor"

class MisCursosView(LoginRequiredMixin, ListView):
    """Vista para mostrar los cursos creados por el profesor"""
    model = Curso
    template_name = "cursos/mis_cursos.html"
    context_object_name = "cursos"

    def get_queryset(self):
        return Curso.objects.filter(profesor=self.request.user)

class DetalleCursoView(LoginRequiredMixin, DetailView):
    """Vista para mostrar los detalles de un curso y permitir la inscripción"""
    model = Curso
    template_name = "cursos/detalle_curso.html"
    context_object_name = "curso"

    def get_queryset(self):
        return Curso.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        context["inscrito"] = Inscripcion.objects.filter(estudiante=usuario, curso=self.object).exists()
        context["lecciones"] = self.object.lecciones.all()  # Agrega esto
        return context

class CrearCursoView(EsProfesorMixin, LoginRequiredMixin, CreateView):
    """Vista para crear un curso"""
    model = Curso
    form_class = CursoForm
    template_name = "cursos/crear_curso.html"

    def form_valid(self, form):
        form.instance.profesor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cursos:mis_cursos")

class EditarCursoView(EsProfesorMixin, LoginRequiredMixin, UpdateView):
    """Vista para editar un curso"""
    model = Curso
    form_class = CursoForm
    template_name = "cursos/editar_curso.html"

    def get_success_url(self):
        return reverse_lazy("cursos:detalle_curso", kwargs={"pk": self.object.pk})

class SeleccionarCursoView(LoginRequiredMixin, ListView):
    """Vista para seleccionar un curso antes de crear una lección"""
    model = Curso
    template_name = "cursos/seleccionar_curso.html"
    context_object_name = "cursos"

    def get_queryset(self):
        return Curso.objects.filter(profesor=self.request.user)

class CrearLeccionView(EsProfesorMixin, LoginRequiredMixin, CreateView):
    """Vista para crear una nueva lección en un curso"""
    model = Leccion
    form_class = LeccionForm
    template_name = "cursos/crear_leccion.html"

    def dispatch(self, request, *args, **kwargs):
        self.curso = get_object_or_404(Curso, id=self.kwargs["curso_id"], profesor=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.curso = self.curso
        form.instance.orden = self.curso.lecciones.count() + 1  # Asigna el orden automáticamente
        response = super().form_valid(form)
        print("Lección creada:", form.instance)  # Agrega esto para depuración
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["curso"] = self.curso
        return context

    def get_success_url(self):
        return reverse_lazy("cursos:detalle_curso", kwargs={"pk": self.kwargs["curso_id"]})
    


class EditarLeccionView(EsProfesorMixin, LoginRequiredMixin, UpdateView):
    """Vista para editar una lección"""
    model = Leccion
    form_class = LeccionForm
    template_name = "cursos/editar_leccion.html"

    def get_queryset(self):
        return Leccion.objects.filter(curso__profesor=self.request.user)

    def get_success_url(self):
        return reverse_lazy("cursos:detalle_curso", kwargs={"pk": self.object.curso.pk})

    def get_context_data(self, **kwargs):
        """Agrega el curso al contexto de la plantilla"""
        context = super().get_context_data(**kwargs)
        context["curso"] = self.object.curso  # Agregamos el curso explícitamente
        return context


class EliminarCursoView(EsProfesorMixin, LoginRequiredMixin, DeleteView):
    """Vista para eliminar un curso"""
    model = Curso
    template_name = "cursos/eliminar_curso.html"
    
    def get_success_url(self):
        return reverse_lazy("cursos:mis_cursos")
    


class DetalleLeccionView(DetailView):
    """Vista para mostrar los detalles de una lección"""
    model = Leccion
    template_name = 'cursos/detalle_leccion.html'
    context_object_name = 'leccion'

    def get_context_data(self, **kwargs):
        """Agrega las evaluaciones de la lección al contexto de la plantilla"""
        context = super().get_context_data(**kwargs)

        # Obtener todas las evaluaciones de la lección
        context["evaluaciones"] = Evaluacion.objects.filter(leccion=self.object)

        return context
    

class VerCursosView(LoginRequiredMixin, ListView):
    """Vista para mostrar los cursos disponibles para estudiantes"""
    model = Curso
    template_name = "cursos/ver_cursos.html"
    context_object_name = "cursos"

    def get_queryset(self):
        return Curso.objects.filter(publicado=True, profesor__rol="profesor")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener cursos en los que el usuario está inscrito
        cursos_inscritos = Inscripcion.objects.filter(estudiante=self.request.user).values_list("curso_id", flat=True)

        print(f"Cursos en los que está inscrito {self.request.user}: {list(cursos_inscritos)}")  # ✅ Verifica en consola

        context["inscritos"] = cursos_inscritos
        return context


    





