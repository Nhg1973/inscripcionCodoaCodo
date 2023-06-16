from django.db import models
from django.utils import timezone
from gestion_personas.models import Alumno, Docente, Tutor

class Categoria(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    photo = models.ImageField(upload_to="categorias")
    eliminada = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre



'''  Relación de uno a muchos:
     relación de uno a muchos con el modelo Categoria a través del campo categoria. 
     Un objeto de Categoria puede estar relacionado con varios objetos de Curso, 
     mientras que un objeto de Curso solo puede estar relacionado con un objeto de Categoria. 
     Esta relación se define mediante la clave externa (ForeignKey) en el campo categoria.

    Relación de muchos a muchos:
    relación de muchos a muchos con el modelo Alumno a través del campo inscriptos. 
    Esto se logra mediante el uso del atributo ManyToManyField. 
    Un objeto de Curso puede tener varios objetos de Alumno inscritos, 
    y un objeto de Alumno puede estar inscrito en varios objetos de Curso. 
    Esta relación se gestiona mediante la tabla de unión Inscripcion, 
    que se especifica a través del atributo through en el campo inscriptos.
'''
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    photo = models.ImageField(upload_to="cursos")
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    docente_titular = models.ForeignKey(Docente, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_cierre = models.DateField()
    cupo = models.PositiveIntegerField()
    inscriptos = models.ManyToManyField(Alumno, through='Inscripcion')

    class Meta:
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nombre


class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return f"{self.nombre} - {self.alumno}"


class Inscripcion(models.Model):
    ESTADO_CHOICES = (
        ('S', 'Solicitado'),
        ('A', 'Aceptado'),
        ('R', 'Rechazado'),
        ('P', 'Pendiente'),
    )
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='S')

    class Meta:
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f"{self.alumno} - {self.curso}"
    
    def aceptar_solicitud(self, curso):
        if curso.cupo > 0:
            curso.cupo -= 1
            curso.save()
            self.estado = 'A'
            self.save()
            Inscripcion.objects.create(alumno=self.alumno, curso=curso, estado='A')


    def pendiente_solicitud(self):
        self.estado = 'P'
        self.save()

    def rechazar_solicitud(self):
        self.estado = 'R'
        self.save()


class SolicitudInscripcion(models.Model):
    ESTADO_CHOICES = (
        ('S', 'Solicitado'),
        ('A', 'Aceptado'),
        ('R', 'Rechazado'),
        ('P', 'Pendiente'),
    )

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='S')

    class Meta:
        verbose_name_plural = "Solicitudes de Inscripción"

    def __str__(self):
       return f"{self.alumno} - {self.curso}"

