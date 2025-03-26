from django.contrib.auth.models import User, Group 
from django.db import models


class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=9, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Usamos usuario como nombre
    # Aquí puedes agregar cualquier otro campo que necesites

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def save(self, *args, **kwargs):
        if not self.usuario:
            try:
                user = User.objects.create_user(
                    username=self.email,  
                    email=self.email,
                    password=self.dni,  
                )
                user.is_staff = True 
                user.save() 

                grupo_profesor, created = Group.objects.get_or_create(name="Profesor")
                
                
                user.groups.add(grupo_profesor)
                
                self.usuario = user  
            except Exception as e:
                print(f"Error al crear usuario para {self.nombre} {self.apellido}: {e}")
        
        # Primero guardamos el Profesor para asignarle un ID
        super().save(*args, **kwargs)
