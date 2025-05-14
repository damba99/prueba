from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

class Usuario(AbstractUser):
    ROLES_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Alumno', 'Alumno'),
        ('Profesor', 'Profesor')
    ]
    rol = models.CharField(max_length=30, choices=ROLES_CHOICES, default='Sin rol')

    # Personaliza los `related_name` para evitar conflictos con el modelo User de Django
    groups = models.ManyToManyField(
        Group,
        related_name='usuarios_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_permissions_set', 
        blank=True
    )
    
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)  # Foto de perfil

    def __str__(self):
        return f"Perfil de {self.usuario.username}"