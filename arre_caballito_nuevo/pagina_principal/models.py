from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

class CodigoRecuperacion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamos con un único usuario
    codigo = models.CharField(max_length=6)  # El código de recuperación
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha en que se generó el código
    activo = models.BooleanField(default=True)  # Campo para saber si el código es válido
    usado = models.BooleanField(default=False) 

    

    def es_valido(self):
        if not self.activo:
            return False
        return True

    @staticmethod
    def generar_codigo(usuario):
        # Invalida cualquier código anterior
        CodigoRecuperacion.objects.filter(usuario=usuario).update(activo=False)

        # Genera un nuevo código de 6 dígitos
        nuevo_codigo = random.randint(100000, 999999)

        # Crea o actualiza el código y lo asigna al usuario
        codigo_obj, creado = CodigoRecuperacion.objects.update_or_create(
            usuario=usuario,
            defaults={'codigo': str(nuevo_codigo), 'activo': True, 'fecha_creacion': timezone.now(), 'usado': False,}
        )

        return nuevo_codigo

