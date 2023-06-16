from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from gestion_cursos.models import Categoria, Curso
from gestion_personas.models import Alumno, Docente, Tutor


def home(request):
    categorias = Categoria.objects.filter(eliminada=False)
    cursos = Curso.objects.filter(activo=True)
    alumnos = Alumno.objects.all()
    profesores = Docente.objects.select_related('user').all()
    titulo = 'Pública'
    context = {
        'categorias': categorias,
        'cursos': cursos,
        'alumnos': alumnos,
        'profesores': profesores,
        'titulo': titulo
    }
    print(context)
    return render(request, 'gestion_publicas/home/index.html', context)

    

def logIn(request):
    titulo = 'Auth'
    context = {
        'titulo': titulo
    }

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'gestion_publicas/auth/pages-login.html', {
                'Error': 'Usuario o Contraseña incorrecta'
            })
        else:
            login(request, user)

            if hasattr(user, 'alumno'):
                if user.alumno.estado == 'Registro':
                    return  redirect('personas:registro')
                else:
                    return  redirect('personas:dashboardAlumnos')
            elif hasattr(user, 'docente'):
                return  redirect('personas:dashboardDocentes')
            elif hasattr(user, 'tutor'):
                return  redirect('personas:dashboardTutores')
            else:
                return render(request, 'gestion_publicas/auth/pages-login.html', {
                    'Error': 'No se encontró el usuario'
                })

    return render(request, 'gestion_publicas/auth/pages-login.html', context)



def logOut(request):
    logout(request)
    return redirect("home")



from django.contrib.auth import authenticate, login

def register(request):
    titulo = 'Auth'
    context = {
        'titulo': titulo
    }

    if request.method == 'GET':
        return render(request, 'gestion_publicas/auth/pages-register.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crear el usuario
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    email=request.POST['email'],
                    password=request.POST['password1']
                )

                # Guardar el usuario
                user.save()

                # Autenticar al usuario recién creado
                authenticated_user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
                if authenticated_user is not None:
                    login(request, authenticated_user)

                # Crear el objeto Alumno asociado al usuario
                alumno = Alumno.objects.create(
                    user=user,
                    estado=Alumno.ESTADO_REGISTRO
                )

                return redirect('personas:registro')
            except:
                return render(request, 'gestion_publicas/auth/pages-register.html', {
                    'Error': 'El Usuario ya existe'
                })
        else:
            return render(request, 'gestion_publicas/auth/pages-register.html', {
                'Error': 'Las contraseñas NO son iguales'
            })


def forgot(request):#falta formulario de recuperacion de contraseña

    return render(request, '#')






