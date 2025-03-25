import os
import django

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arre_caballito.settings')
django.setup()
from django.contrib.auth.models import Group

# Crear los grupos si no existen
def crear_grupos():
    if not Group.objects.filter(name='Admin').exists():
        Group.objects.create(name='Admin')
    if not Group.objects.filter(name='Profesor').exists():
        Group.objects.create(name='Profesor')
    if not Group.objects.filter(name='Alumno').exists():
        Group.objects.create(name='Alumno')

# Llamar a la función al iniciar el proyecto


            
        
if __name__ == "__main__":
    # Imprimir todos los alumnos
    crear_grupos()
