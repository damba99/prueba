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

    def save(self, *args, **kwargs):
        # Crear el nombre de la clase concatenando la disciplina, categoría y el rango horario
        self.nombre = f"{self.id_disciplina.nombre} - {self.id_categoria.nombre}"
        super().save(*args, **kwargs)  # Guardar el objeto después de asignar el nombre

    def __str__(self):
        return f"Clase {self.nombre}"
    
class Sesion(models.Model):
    MAÑANA = 'Mañana' 
    TARDE = 'Tarde'
    
    TURNO_CHOISES = [
        (MAÑANA, 'Mañana'),
        (TARDE, 'Tarde'),
    ]
    
    id_sesion = models.AutoField(primary_key=True)
    id_clase = models.ForeignKey(Clase, related_name='sesiones', on_delete=models.CASCADE)
    id_profesor = models.ForeignKey(Profesor, related_name='clases', on_delete=models.CASCADE, blank=True, null=True)
    dia = models.CharField(max_length=10)
    turno = models.CharField(max_length=10, choices=TURNO_CHOISES, null=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('id_clase', 'dia', 'turno', 'hora_inicio', 'id_profesor')  # Evitar duplicados en el mismo día y hora

    def __str__(self):
        return f"{self.id_clase.nombre} - {self.dia} - {self.turno} - {self.hora_inicio.strftime('%H:%M')}-{self.hora_fin.strftime('%H:%M')} - Prof.:{self.id_profesor.nombre} {self.id_profesor.apellido}"


