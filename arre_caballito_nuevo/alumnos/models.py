from django.db import models
from django.contrib.auth.models import User
from usuarios.models import Usuario

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=9, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)    
    telefono = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True)  # Usa tu modelo Usuario personalizado

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        # Crear un usuario solo si no existe ya
        if not self.usuario:  # Si el Alumno aún no tiene usuario asignado
            print("sin usuario")
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
        super().save(*args, **kwargs)
