from django.shortcuts import get_object_or_404, redirect, render
from gestion_cursos.models import Curso, Inscripcion
from gestion_personas.models import Alumno, Docente, Tutor
from .formrs.user_registration_form import ProfileEditForm
from django.db.models import Count, ExpressionWrapper, F, IntegerField
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib import messages

def registro(request):
    titulo = 'Registro'
    context = {'titulo': titulo}
    
    if request.method == 'GET':
        form = ProfileEditForm()
        context['form'] = form  # Incluir el formulario en el contexto
        return render(request, 'gestion_personas/users-profile.html', context)


    elif request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            firstname = form.cleaned_data['nombre']
            lastname = form.cleaned_data['apellido']

            # Guardar el nombre y apellido en el modelo User
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            # Verificar si el usuario ya tiene un Alumno asociado
            try:
                alumno = Alumno.objects.get(user=user)
                alumno.estudio = form.cleaned_data['estudio']
                alumno.trabajo = form.cleaned_data['trabajo']
                alumno.pais = form.cleaned_data['pais']
                alumno.direccion = form.cleaned_data['direccion']
                alumno.telefono = form.cleaned_data['telefono']
                alumno.twitter = form.cleaned_data['twitter']
                alumno.facebook = form.cleaned_data['facebook']
                alumno.linkedin = form.cleaned_data['linkedin']
                if form.cleaned_data['foto']:
                    alumno.photo = form.cleaned_data['foto']
                alumno.estado = Alumno.ESTADO_DATOS_BASICOS  # Modificar el estado a "Datos básicos"
                alumno.save()  # Guardar el cambio del estado en la base de datos

            except Alumno.DoesNotExist:
                alumno = form.save(commit=False)
                alumno.user = user
                alumno.save()

            return redirect('personas:dashboardAlumnos')

        else:
            messages.error(request, 'Hubo un error en el formulario. Por favor, corrige los errores.')
            context['form'] = form
            return render(request, 'gestion_personas/users-profile.html', context)

    else:
        return render(request, 'gestion_personas/auth/pages-register.html', {'error': 'Las de contenido'}, context)


def dashboardAlumnos(request):

    user = request.user
    alumno = Alumno.objects.get(user=user)
    # Obtiene el contenido del contexto de la vista dashboardAlumnos
    cursos = Curso.objects.all()
    profesores = Docente.objects.all()
    context = {
        'cursos': cursos,
        'profesores': profesores,
        'titulo': 'Dashboard Alumnos',
        'user': user,
        'alumno': alumno, 
        'photo': alumno.photo
    }
    return render(request, 'gestion_personas/dashboardAlumnos.html', context)


def dashboardDocentes(request):
    user = request.user
    docente = Docente.objects.get(user=user)
    cursos = Curso.objects.filter(docente_titular=docente)
    cursos_con_alumnos = {}
    for curso in cursos:
        inscripciones = Inscripcion.objects.filter(curso=curso)
        alumnos = [inscripcion.alumno for inscripcion in inscripciones]
        cursos_con_alumnos[curso.nombre] = alumnos 
    context = {
            'titulo':'Dashboard Docentes',
            'user': user,
            'docente': docente,
            'cursos_con_alumnos': cursos_con_alumnos,
            'photo':docente.photo
    }
    return render(request, 'gestion_personas/dashboardDocentes.html', context)
     

def dashboardTutores(request):

    user = request.user
    docentes = Docente.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()
    docente = Tutor.objects.get(user=user)
    cursos_con_alumnos = {}
    for curso in cursos:
        inscripciones = Inscripcion.objects.filter(curso=curso)
        alumnos = [inscripcion.alumno for inscripcion in inscripciones]
        cursos_con_alumnos[curso.nombre] = alumnos               
    context = {
            'titulo':'Dashboard Tutores',
            'user': user,
            'alumnos' :  alumnos,
            'docentes': docente,
            'cursos_con_alumnos': cursos_con_alumnos,
            'photo':docente.photo
    }
    return render(request, 'gestion_personas/dashboardTutores.html', context)

# Alumnos 


class AlumnoListView(ListView):
    model = Alumno
    template_name = 'gestion_personas/ver_alumnos.html'
    context_object_name = 'alumnos'

    def get_queryset(self):
        cursos = Curso.objects.all()  # Obtener todos los cursos
        alumnos = Alumno.objects.filter(inscripcion__curso__in=cursos).distinct()  # Filtrar los alumnos inscritos en los cursos y aplicar distinct()

        # Imprimir por consola el resultado
        for alumno in alumnos:
            cursos_inscritos = alumno.inscripcion_set.values_list('curso__nombre', flat=True).distinct()
            for curso in cursos_inscritos:
                print(f"Alumno: {alumno} - Curso inscrito: {curso}")

        return alumnos
    


class AlumnosDocenteListView(ListView):
    model = Alumno
    template_name = 'gestion_personas/ver_alumnos_docente.html'
    context_object_name = 'alumnos'

    def get_queryset(self):
        # Obtener el docente actual
        docente_actual = self.request.user.docente

        # Filtrar los cursos que pertenecen al docente actual
        cursos_docente = Curso.objects.filter(docente_titular=docente_actual)

        # Filtrar los alumnos inscritos en los cursos del docente actual
        queryset = Alumno.objects.filter(inscripcion__curso__in=cursos_docente)

        # Imprimir los resultados por consola
        for alumno in queryset:
            cursos = alumno.inscripcion_set.filter(curso__in=cursos_docente)
            print(f"Alumno: {alumno}")
            print("Cursos inscritos:")
            for curso in cursos:
                print(f"- {curso.curso.nombre}")

        return queryset



