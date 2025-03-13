from django.db import models
from django.core.exceptions import ValidationError

from clases.models import Categoria, Disciplina
from alumnos.models import Alumno
from caballos.models import Caballo
class Competencia(models.Model):
    id_competencias = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    lugar = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()

    def __str__(self):
        return self.nombre
    
class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    id_competencia = models.ForeignKey(Competencia, related_name='eventos', on_delete=models.CASCADE)
    id_disciplina = models.ForeignKey(Disciplina, related_name='eventos', on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Categoria, related_name='eventos', on_delete=models.CASCADE)

class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)

    id_competencia = models.ForeignKey(Competencia, related_name='inscripciones', on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, related_name='inscripciones', on_delete=models.CASCADE)
    id_caballo = models.ForeignKey(Caballo, related_name='inscripciones', on_delete=models.CASCADE, null=True, blank=True)
    id_evento = models.ForeignKey(Evento, related_name='inscripciones', on_delete=models.CASCADE)

    def clean(self):
        super().clean()
        # Si el caballo no es null, verifica que la disciplina del caballo coincida con la del evento
        if self.id_caballo:
            # Verificar si el caballo pertenece a la disciplina del evento
            if self.id_evento.id_disciplina not in self.id_caballo.disciplinas.all():
                raise ValidationError(f"El caballo {self.id_caballo.nombre} no está registrado en la disciplina del evento.")
            
    def __str__(self):
        return f"Inscripción {self.id_inscripcion} - Alumno {self.id_alumno.nombre} - Competencia {self.id_competencia.nombre} - Evento {self.id_evento.id_evento}"

