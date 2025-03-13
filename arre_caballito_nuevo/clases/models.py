from django.db import models
from django.core.exceptions import ValidationError
from profesores.models import Profesor
from caballos.models import Caballo, Disciplina
from alumnos.models import Alumno


class Categoria(models.Model):
    PONY = 'Pony'
    ESCUELITA = 'Escuelita'
    ESCUELA = 'Escuela'
    
    CATEGORIA_CHOICES = [
        (PONY, 'Pony'),
        (ESCUELITA, 'Escuelita'),
        (ESCUELA, 'Escuela'),
    ]

    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, choices=CATEGORIA_CHOICES)

    def __str__(self):
        return self.nombre


class Clase(models.Model):
    id_clase = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    id_profesor = models.ForeignKey(Profesor, related_name='clases', on_delete=models.CASCADE, blank=True, null=True)
    id_disciplina = models.ForeignKey(Disciplina, related_name='clases', on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Categoria, related_name='clases', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Crear el nombre de la clase concatenando la disciplina, categoría y hora de inicio
        self.nombre = f"{self.id_disciplina.nombre} - {self.id_categoria.nombre} - {self.fecha.strftime('%d-%m-%Y')} - {self.hora_inicio.strftime('%H:%M')}"
        super().save(*args, **kwargs)  # Guardar el objeto después de asignar el nombre

    def __str__(self):
        return f"Clase {self.nombre}"

class Asistencia(models.Model):
    id_clase = models.ForeignKey(Clase, related_name='asistencias', on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, related_name='asistencias', on_delete=models.CASCADE)
    id_caballo = models.ForeignKey(Caballo, related_name='asistencias', on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        if self.id_caballo:
            # Verificar si el caballo pertenece a la disciplina de la clase
            if self.id_disciplina not in self.id_caballo.disciplinas.all():
                raise ValidationError(f"El caballo {self.id_caballo.nombre} no está inscrito en la disciplina de esta clase.")
            
    def save(self, *args, **kwargs):
        self.clean()  # Realiza la validación antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Asistencia Clase {self.id_clase.id_clase} - Alumno {self.id_alumno.nombre} - Caballo {self.id_caballo.nombre if self.id_caballo else 'Ninguno'}"



