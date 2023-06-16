from django.urls import path
from .views import *

app_name = 'personas'

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('dashAlumnos/', dashboardAlumnos, name='dashboardAlumnos'),
    path('dashDocentes/', dashboardDocentes, name='dashboardDocentes'),
    path('dashTutores/', dashboardTutores, name='dashboardTutores'),

    #Alumnos
    path('alumnos/', AlumnoListView.as_view(), name='ver_alumnos'),
    path('alumnos/docente/', AlumnosDocenteListView.as_view(), name='ver_alumnos_docente'),
]
