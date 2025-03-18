import os
import django
from django.conf import settings
from alumnos.models import Alumno

# Configurar el entorno de Django (esto debe estar antes de cualquier llamada a la base de datos)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arre_caballito.settings')
django.setup()

def imprimir_alumnos():
    alumnos = Alumno.objects.all()
    for alumno in alumnos:
        print(alumno.nombre)

# Ejecutar la función
if __name__ == "__main__":
    imprimir_alumnos()


