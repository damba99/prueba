from django.db import models
from django.contrib.auth.models import User
from usuarios.models import Usuario
from caballos.models import Caballo
from clases.models import Clase, Categoria
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
    
class Asistencia(models.Model):
    id_clase = models.ForeignKey(Clase, related_name='asistencias', on_delete=models.CASCADE)
    id_alumno = models.ForeignKey(Alumno, related_name='asistencias', on_delete=models.CASCADE)
    id_caballo = models.ForeignKey(Caballo, related_name='asistencias', on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(default=timezone.now)

    def clean(self):
        super().clean()
        
        # Verificar si el alumno está asociado a la clase
        if self.id_clase not in self.id_alumnos.id_clases.all():
            raise ValidationError(f"El alumno {self.id_alumno.nombre} no está inscrito en esta clase.")
        
        if self.id_caballo:
            # Verificar si el caballo pertenece a la disciplina de la clase
            if self.id_clase.id_disciplina not in self.id_caballo.disciplinas.all():
                raise ValidationError(f"El caballo {self.id_caballo.nombre} no está inscrito en la disciplina de esta clase.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Realiza la validación antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Asistencia Clase {self.id_clase.id_clase} - Alumno {self.id_alumno.nombre} - Caballo {self.id_caballo.nombre if self.id_caballo else 'Ninguno'}"