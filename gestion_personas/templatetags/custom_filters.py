from django import template
from django.utils import timezone


register = template.Library()

@register.filter
def filtro_fecha_cierre(cursos):
    fecha_actual = timezone.now().date()
    return [curso for curso in cursos if curso.fecha_cierre >= fecha_actual]

