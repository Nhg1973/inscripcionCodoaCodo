from django.db import models
from django.contrib.auth.models import User

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="tutor", default='defaul.jpg')

    def __str__(self):
        return f"Tutor @{self.user.username}"

    class Meta:
        verbose_name_plural = "Tutores"

class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="docentes", default='defaul.jpg')

    def __str__(self):
        return f"Docente @{self.user.username}"
    
    class Meta:
        verbose_name_plural = "Docentes"


class Alumno(models.Model):
    ESTADO_REGISTRO = 'Registro'
    ESTADO_DATOS_BASICOS = 'Datos básicos'
    ESTADO_INSCRITO = 'Inscrito'
    ESTADO_ACEPTADO = 'Aceptado'

    ESTADOS_ALUMNO = [
        (ESTADO_REGISTRO, 'Registro'),
        (ESTADO_DATOS_BASICOS, 'Datos básicos'),
        (ESTADO_INSCRITO, 'Inscrito'),
        (ESTADO_ACEPTADO, 'Aceptado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="alumno", default='default.jpg')
    estudio = models.TextField(blank=True, null=True)
    trabajo = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_ALUMNO, default=ESTADO_REGISTRO)

    def __str__(self):
        return f"Alumno @{self.user.username}"

    class Meta:
        verbose_name_plural = "Alumnos"
