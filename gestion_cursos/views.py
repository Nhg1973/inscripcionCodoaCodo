from django.shortcuts import redirect, render
from .models import Categoria, Curso, Inscripcion
from django.db.models import Count, ExpressionWrapper, F, IntegerField
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Categoria, SolicitudInscripcion
from gestion_personas.models import Alumno, Docente, Tutor

# CATEGORIAS

def es_tutor(user):
    return user.is_authenticated and hasattr(user, 'tutor')

def es_docente(user):
    return user.is_authenticated and hasattr(user, 'docente')


@method_decorator(user_passes_test(es_tutor), name='dispatch')
class CategoriaCreateView(CreateView):
    model = Categoria
    fields = ['nombre', 'descripcion', 'photo']
    template_name = 'gestion_cursos/create_and_edit_categorias.html'
    success_url = reverse_lazy('personas:dashboardTutores')

    def form_valid(self, form):
        # Asignamos el tutor actual como el tutor de la nueva categoría
        form.instance.tutor = self.request.user.tutor

        try:
            # Llamamos al método `form_valid` del padre para guardar la categoría en la base de datos
            response = super().form_valid(form)
            messages.success(self.request, 'Categoría creada exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al crear categoría: {e}')
            return self.form_invalid(form)

        # Redirigimos a la página de dashboard después de crear la categoría
        return redirect('personas:dashboardTutores')


    
@method_decorator(user_passes_test(es_tutor), name='dispatch')
class CategoriaUpdateView(UpdateView):
    model = Categoria
    fields = ['nombre', 'descripcion', 'photo']
    template_name = 'gestion_cursos/create_and_edit_categorias.html'
    success_url = reverse_lazy('personas:dashboardTutores')

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, 'Categoría actualizada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar categoría: {e}')
        return redirect('personas:dashboardTutores')
    
    def form_valid(self, form):
        form.instance.tutor = self.request.user.tutor
        return super().form_valid(form)

  
@method_decorator(user_passes_test(es_tutor), name='dispatch')
class CategoriaDeleteView(DeleteView):
    model = Categoria
    fields = ['nombre', 'descripcion', 'photo']
    template_name = 'gestion_cursos/create_and_edit_categorias.html'
    success_url = reverse_lazy('cursos:lista_categorias')

    def post(self, request, *args, **kwargs):
        categoria = self.get_object()
        categoria.eliminada = True
        categoria.save()
        messages.success(request, 'Categoría suspendida exitosamente.')
        return redirect(self.success_url)

@method_decorator(user_passes_test(es_tutor), name='dispatch')
class CategoriaAltaView(DeleteView):
    model = Categoria
    fields = ['nombre', 'descripcion', 'photo']
    template_name = 'gestion_cursos/create_and_edit_categorias.html'
    success_url = reverse_lazy('cursos:lista_categorias')

    def post(self, request, *args, **kwargs):
        categoria = self.get_object()
        categoria.eliminada = False
        categoria.save()
        messages.success(request, 'Categoría dada de alta exitosamente.')
        return redirect(self.success_url)

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'gestion_cursos/categorias.html'


#CURSOS

class CursoListView(ListView):
    model = Curso
    template_name = 'gestion_cursos/cursos.html'
    context_object_name = 'cursos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos_inactivos'] = Curso.objects.filter(activo=False)

        user = self.request.user

        if es_tutor(user):
            # Si el usuario es un tutor, se muestran todos los cursos
            context['cursos'] = Curso.objects.all()
        elif es_docente(user):
            # Si el usuario es un docente, se filtran los cursos por el docente titular
            docente_titular = user.docente
            context['cursos'] = Curso.objects.filter(docente_titular=docente_titular)

        return context

        

class CursoCreateView(CreateView):
    model = Curso
    template_name = 'gestion_cursos/cretaedit_cursos.html'
    fields = ['nombre', 'descripcion', 'photo', 'fecha_creacion', 'activo', 'categoria', 'docente_titular', 'fecha_inicio', 'fecha_cierre', 'cupo']
    success_url = reverse_lazy('personas:dashboardTutores')

    def form_valid(self, form):
        try:
            # Llamamos al método `form_valid` del padre para guardar el curso en la base de datos
            response = super().form_valid(form)
            messages.success(self.request, 'Curso creada exitosamente.')
        except Exception as e:
            messages.error(self.request, f'Error al crear curso: {e}')
            return self.form_invalid(form)

        # Redirigimos a la página de dashboard después de crear la categoría
        return redirect('personas:dashboardTutores')

class CursoUpdateView(UpdateView):
    model = Curso
    template_name = 'gestion_cursos/cretaedit_cursos.html'
    fields = ['nombre', 'descripcion', 'photo', 'fecha_creacion', 'activo', 'categoria', 'docente_titular', 'fecha_inicio', 'fecha_cierre', 'cupo']
    success_url = reverse_lazy('personas:dashboardTutores')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'El curso se ha actualizado exitosamente.')
        return response

# Inscripciones

# Alumnos solicitan inscripcion

def solicitud_inscripcion(request, curso_id):
    if request.method == 'POST':
        alumno_id = request.POST.get('alumno_id')
        curso = Curso.objects.get(id=curso_id)
        alumno = Alumno.objects.get(id=alumno_id)
        solicitud_existente = SolicitudInscripcion.objects.filter(alumno=alumno, curso=curso).exists()
        if not solicitud_existente:
            solicitud = SolicitudInscripcion(alumno=alumno, curso=curso)
            solicitud.save()
            messages.success(request, 'La solicitud de inscripción se ha enviado correctamente.')
        else:
            messages.error(request, 'Ya existe una solicitud de inscripción para este curso.')
        return redirect('personas:dashboardAlumnos')
    else:
        curso = Curso.objects.get(id=curso_id)
        alumnos = Alumno.objects.all()
        return render(request, 'personas:dashboardAlumnos.html', {'curso': curso, 'alumnos': alumnos})
    
# Tutor gestiona inscripciones
# lista de solicitudes

class SolicitudesListView(ListView):
    model = SolicitudInscripcion
    template_name = 'gestion_cursos/solicitudes_lista.html'
    context_object_name = 'solicitudes'

    def get_queryset(self):
        queryset = SolicitudInscripcion.objects.annotate(
            cupo_disponible=ExpressionWrapper(F('curso__cupo') - Count('curso__inscriptos'), output_field=IntegerField()),
            inscriptos_count=Count('curso__inscriptos')
        ).order_by('curso', 'fecha_solicitud').filter(estado='S')

        # Imprimir resultados por consola
        for solicitud in queryset:
            print(f"Curso: {solicitud.curso}, Cupo Disponible: {solicitud.cupo_disponible}, Inscriptos: {solicitud.inscriptos_count}")

        return queryset

    
# Gestion de solicitudes 

def aceptar_solicitud(request, solicitud_id):
    solicitud = SolicitudInscripcion.objects.get(id=solicitud_id)
    curso = solicitud.curso  # Obtener el curso correspondiente a la solicitud
    alumno = solicitud.alumno  # Obtener el alumno de la solicitud
    
    if Inscripcion.objects.filter(alumno=alumno, curso=curso).exists():
        # La inscripción ya existe, mostrar mensaje de error
        messages.error(request, 'El alumno ya está inscrito en este curso.')
    else:
        inscripcion = Inscripcion.objects.create(alumno=alumno, curso=curso, estado='A')
        
        solicitud.estado = 'A'  # Actualizar el estado de la solicitud
        solicitud.save()
    
    return redirect('cursos:solicitudes_lista')

def pendiente_solicitud(request, solicitud_id):
    solicitud = SolicitudInscripcion.objects.get(id=solicitud_id)
    solicitud.estado = 'P'  # Actualizar el estado a "Pendiente"
    solicitud.save()
    return redirect('cursos:solicitudes_lista')

def rechazar_solicitud(request, solicitud_id):
    solicitud = SolicitudInscripcion.objects.get(id=solicitud_id)
    solicitud.estado = 'R'  # Actualizar el estado a "Rechazado"
    solicitud.save()
    return redirect('cursos:solicitudes_lista')

 