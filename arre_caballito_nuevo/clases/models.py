from django.db import models
from profesores.models import Profesor
from caballos.models import  Disciplina


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
    nombre = models.CharField(max_length=255, blank=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    id_profesor = models.ForeignKey(Profesor, related_name='clases', on_delete=models.CASCADE, blank=True, null=True)
    id_disciplina = models.ForeignKey(Disciplina, related_name='clases', on_delete=models.CASCADE)
    id_categoria = models.ForeignKey(Categoria, related_name='clases', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Crear el nombre de la clase concatenando la disciplina, categoría y el rango horario
        if self.hora_inicio and self.hora_fin:  # Asegurarse de que las horas no sean None
            self.nombre = f"{self.id_disciplina.nombre} - {self.id_categoria.nombre} - {self.hora_inicio.strftime('%H:%M')}-{self.hora_fin.strftime('%H:%M')}"
        super().save(*args, **kwargs)  # Guardar el objeto después de asignar el nombre

    def __str__(self):
        return f"Clase {self.nombre}"


