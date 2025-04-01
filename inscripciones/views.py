from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Curso,Inscripcion
from django.views.generic import DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.urls import reverse


class InscribirseCursoView(LoginRequiredMixin, View):
    """Vista para que un estudiante se inscriba en un curso"""

    def post(self, request, curso_id):
        curso = get_object_or_404(Curso, id=curso_id, publicado=True)
        
        # Verificar si ya está inscrito
        if Inscripcion.objects.filter(estudiante=request.user, curso=curso).exists():
            messages.warning(request, "Ya estás inscrito en este curso.")
        else:
            Inscripcion.objects.create(estudiante=request.user, curso=curso)
            messages.success(request, f"Te has inscrito en {curso.nombre} correctamente.")

        return HttpResponseRedirect(reverse("cursos:detalle_curso", kwargs={"pk": curso_id}))