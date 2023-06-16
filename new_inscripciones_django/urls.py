from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_publicas.urls')),
    path('personas/', include('gestion_personas.urls', namespace='personas')),
    path('cursos/', include('gestion_cursos.urls', namespace='cursos')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Ruta para servir los archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
