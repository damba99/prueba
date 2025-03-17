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
    def sesiones(self):
        # Obtiene las sesiones del alumno a través del modelo intermedio AlumnoSesion
        return Sesion.objects.filter(alumnosesion__alumno=self)
    
class AlumnoSesion(models.Model):
    alumno = models.ForeignKey(Alumno, related_name='sesiones', on_delete=models.CASCADE)
    sesion = models.ForeignKey(Sesion, related_name='alumnos', on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)  # Fecha en que el alumno se inscribió

    class Meta:
        unique_together = ('alumno', 'sesion')  # Aseguramos que un alumno no se inscriba en la misma sesión más de una vez

    def __str__(self):
        return f"{self.alumno} inscrito en {self.sesion}"
    
class Asistencia(models.Model):
    id_sesion = models.ForeignKey(Sesion, related_name='asistencias', on_delete=models.CASCADE, null=True)
    id_alumno = models.ForeignKey(Alumno, related_name='asistencias', on_delete=models.CASCADE)
    id_caballo = models.ForeignKey(Caballo, related_name='asistencias', on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(default=timezone.now)

    def clean(self):
        super().clean()

        # Verificar si el alumno está inscrito en la sesión
        # Usamos el modelo AlumnoSesion para verificar la relación
        if not AlumnoSesion.objects.filter(alumno=self.id_alumno, sesion=self.id_sesion).exists():
            raise ValidationError(f"El alumno {self.id_alumno.nombre} no está inscrito en la sesión {self.id_sesion.id_clase.nombre}.")

        # Verificar si el caballo está asociado a la disciplina de la clase de la sesión
        if self.id_caballo:
            # Accedemos a la clase de la sesión
            clase_sesion = self.id_sesion.id_clase
            # Verificamos si la disciplina de la clase está en las disciplinas del caballo
            if self.id_caballo.disciplinas.filter(id=clase_sesion.id_disciplina.id).exists() is False:
                raise ValidationError(f"El caballo {self.id_caballo.nombre} no está asociado a la disciplina {clase_sesion.id_disciplina.nombre} de esta sesión.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Realiza la validación antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Asistencia Clase {self.id_sesion.id_clase.id_clase} - Alumno {self.id_alumno.nombre} - Caballo {self.id_caballo.nombre if self.id_caballo else 'Ninguno'}"