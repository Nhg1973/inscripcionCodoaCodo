from django.urls import path
from .views import *

app_name = 'cursos'


urlpatterns = [
    #CATEGORIAS
    path('categoria/crear/', CategoriaCreateView.as_view(), name='crear_categoria'),
    # VISTAS PARAMETRIZADAS, en la ruta path('categoria/<int:pk>/editar/', CategoriaUpdateView.as_view(), 
    # name='editar_categoria'), cuando accedas a una URL como "/categoria/1/editar/", 
    # el número 1 se capturará como el valor del parámetro "pk" 
    # y se pasará a la vista CategoriaUpdateView para su procesamiento.
    path('categoria/<int:pk>/editar/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('categoria/<int:pk>/eliminar/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    path('categoria/<int:pk>/alta/', CategoriaAltaView.as_view(), name='dar_alta_categoria'),
    path('categorias/', CategoriaListView.as_view(), name='lista_categorias'),
    #CURSOS
    path('cursos/', CursoListView.as_view(), name='lista_cursos'),
    path('cursos/crear/', CursoCreateView.as_view(), name='crear_curso'),
    path('curso/<int:pk>/editar/', CursoUpdateView.as_view(), name='editar_curso'),
    #INSCRIPCION
    path('curso/<int:curso_id>/solicitud/', solicitud_inscripcion, name='solicitud_inscripcion'),
    path('solicitudes/', SolicitudesListView.as_view(), name='solicitudes_lista'),
    path('solicitud/<int:solicitud_id>/aceptar/', aceptar_solicitud, name='aceptar_solicitud'),
    path('solicitud/<int:solicitud_id>/pendiente/', pendiente_solicitud, name='pendiente_solicitud'),
    path('solicitud/<int:solicitud_id>/rechazar/', rechazar_solicitud, name='rechazar_solicitud'),

]
