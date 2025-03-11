from django.db import models

class Caballo(models.Model):
    id_caballo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Macho'), ('H', 'Hembra')])

    def __str__(self):
        return self.nombre