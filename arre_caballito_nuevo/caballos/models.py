from django.db import models
from clases.models import Disciplina

class Caballo(models.Model):
    id_caballo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Macho'), ('H', 'Hembra')])
    
    def __str__(self):
        return self.nombre
    
class CaballoDisciplina(models.Model):
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.caballo.nombre} - {self.disciplina.nombre}'