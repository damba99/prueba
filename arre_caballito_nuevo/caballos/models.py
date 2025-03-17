from django.db import models
from clases.models import Disciplina

class Caballo(models.Model):
    id_caballo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Macho'), ('H', 'Hembra')])
    disciplinas = models.ManyToManyField(Disciplina)

    def __str__(self):
        return self.nombre
    
