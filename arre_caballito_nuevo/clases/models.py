from django.db import models
from profesores.models import Profesor

class Categoria(models.Model):

    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Clase(models.Model):
    id_clase = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True)
    id_disciplina = models.ForeignKey(Disciplina, related_name='clases', on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Categoria, related_name='clases', on_delete=models.CASCADE)
    activo = models.BooleanField(default=True) 
    def __str__(self):
        return f"Clase {self.nombre}"
    
class Sesion(models.Model):
    LUNES = 'Lunes'
    MARTES = 'Martes'
    MIERCOLES = 'Miércoles'
    JUEVES = 'Jueves'
    VIERNES = 'Viernes'
    SABADO = 'Sábado'
    DOMINGO = 'Domingo'
    
    DIA_CHOICES = [
        (LUNES, 'Lunes'),
        (MARTES, 'Martes'),
        (MIERCOLES, 'Miércoles'),
        (JUEVES, 'Jueves'),
        (VIERNES, 'Viernes'),
        (SABADO, 'Sábado'),
        (DOMINGO, 'Domingo'),
    ]
    id_sesion = models.AutoField(primary_key=True)
    id_profesor = models.ForeignKey(Profesor, related_name='sesiones', on_delete=models.CASCADE, blank=True, null=True)
    dia = models.CharField(max_length=10, choices=DIA_CHOICES)
    id_clase = models.ForeignKey(Clase, related_name='sesiones', on_delete=models.CASCADE, null=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('dia', 'id_clase', 'hora_inicio', 'id_profesor')  # Evitar duplicados en el mismo día y hora

    def __str__(self):
        return f"{self.id_clase.nombre} - {self.dia} - {self.hora_inicio.strftime('%H:%M')}-{self.hora_fin.strftime('%H:%M')} - Prof.:{self.id_profesor.nombre} {self.id_profesor.apellido}"


