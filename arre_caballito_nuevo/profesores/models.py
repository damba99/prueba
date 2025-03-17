from django.db import models
from usuarios.models import Usuario

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=9, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        if not self.usuario:  # Si el Profesor aún no tiene usuario asignado
            # Crear el usuario con el mismo correo que el profesor y DNI como contraseña
            user = Usuario.objects.create(
                username=self.email,  # Usar el email del Profesor como nombre de usuario
                email=self.email,
                password=self.dni,  # Usar el DNI del Profesor como contraseña
                rol='Profesor'  # Asignar el rol de 'Profesor'
            )
            self.usuario = user

        super().save(*args, **kwargs)
