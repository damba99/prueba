from django.db import models
from django.contrib.auth.models import User
from usuarios.models import Usuario
from caballos.models import Caballo
from clases.models import Clase, Categoria, Sesion
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=9, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)    
    telefono = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    id_categoria = models.ForeignKey(Categoria, related_name='alumnos', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        # Crear un usuario solo si no existe ya
        if not self.usuario:  # Si el Alumno aún no tiene usuario asignado
            try:
                # Crear el usuario con el mismo correo que el alumno y DNI como contraseña
                user = Usuario.objects.create( 
                    username=self.email,
                    email=self.email,
                    password=self.dni,
                    rol='Alumno'
                )
                self.usuario = user  # Asignar el usuario creado al Alumno
            except Exception as e:
                print(f"Error al crear usuario para {self.nombre} {self.apellido}: {e}")
        
        # Primero guardamos el Alumno para asignarle un ID
        super().save(*args, **kwargs)

    @property
    def clases(self):
        # Obtiene las clases en las que el alumno está inscrito a través del modelo intermedio AlumnoClase
        return Clase.objects.filter(alumnoclase__alumno=self)
    
class AlumnoClase(models.Model):
    alumno = models.ForeignKey(Alumno, related_name='clases', on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, related_name='alumnos', on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)  # Fecha en que el alumno se inscribió

    class Meta:
        unique_together = ('alumno', 'clase') 
        
    def __str__(self):
        return f"{self.alumno} inscrito en {self.clase}"
    
class Asistencia(models.Model):
    id_sesion = models.ForeignKey(Sesion, related_name='asistencias', on_delete=models.CASCADE, null=True)
    id_alumno = models.ForeignKey(Alumno, related_name='asistencias', on_delete=models.CASCADE)
    id_caballo = models.ForeignKey(Caballo, related_name='asistencias', on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(default=timezone.now)

    def clean(self):
        # Asegurarse de que el alumno está inscrito en la clase asociada a la sesión
        # Obtener la clase asociada a la sesión
        if self.id_sesion:
            clase = self.id_sesion.id_clase  # Obtener la clase a la que pertenece la sesión
            
            # Verificar si el alumno está inscrito en esa clase
            if not AlumnoClase.objects.filter(alumno=self.id_alumno, clase=clase).exists():
                raise ValidationError(f"El alumno {self.id_alumno} no está inscrito en la clase {clase}.")
    
    def save(self, *args, **kwargs):
        # Llamar al método clean para validar la asistencia
        self.clean()

        # Si la validación es exitosa, guardar la instancia
        super(Asistencia, self).save(*args, **kwargs)

    def __str__(self):
        return f"Asistencia de {self.id_alumno} a la sesión {self.id_sesion} en {self.fecha}"