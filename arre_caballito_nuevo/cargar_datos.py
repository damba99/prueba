import os
import subprocess
import glob
from django.conf import settings
import django
import importlib.util
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arre_caballito.settings')
django.setup()


def crear_superusuario():
    """Crea un superusuario automáticamente si no existe uno."""
    User = get_user_model()  # Usamos el modelo de usuario configurado en Django (por defecto User)

    if not User.objects.filter(username='admin').exists():
        # Crear el superusuario
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@mail.com',
                password='admin'
            )
            print("Superusuario 'admin' creado correctamente.")
        except Exception as e:
            print(f"Error al crear el superusuario: {e}")
    else:
        print("El superusuario 'admin' ya existe.")


def cargar_todos_los_fixtures():
    """Carga todos los fixtures JSON en las carpetas de fixtures de todas las aplicaciones en el orden específico."""

    # Define el orden de las aplicaciones que deben cargarse primero
    orden_inicio_apps = [
        'usuarios',  # Primero cargamos 'usuarios'
        'caballos',  # Luego 'caballos'
        'profesores',
        'clases', # Después 'profesores'
        'alumnos',  # Y finalmente 'alumnos'
    ]

    # Obtiene las aplicaciones restantes (sin las primeras 4 que ya están en orden)
    apps_restantes = [app for app in settings.INSTALLED_APPS if app not in orden_inicio_apps]

    # Combina las aplicaciones en el orden correcto: primero las 4 definidas, luego el resto
    apps_cargar = orden_inicio_apps + apps_restantes

    # Iteramos sobre el orden de aplicaciones definido
    for app in apps_cargar:
        print(f"Cargando fixtures para la aplicación: {app}")
        try:
            # Importamos dinámicamente el módulo de la app usando importlib
            app_spec = importlib.util.find_spec(app)
            if app_spec is None:
                print(f"La aplicación {app} no se puede importar, se omite.")
                continue

            app_module = importlib.import_module(app)
            
            # Obtenemos el path de la aplicación
            app_dir = os.path.dirname(app_module.__file__)
            
            # Obtenemos el directorio de los fixtures de la app
            fixtures_dir = os.path.join(app_dir, 'fixtures')
            if not os.path.exists(fixtures_dir):
                continue

            # Buscar todos los archivos JSON de fixtures en el directorio de la app
            fixtures_files = glob.glob(os.path.join(fixtures_dir, '*.json'))

            if not fixtures_files:
                continue

            # Cargar cada fixture
            for fixture_file in fixtures_files:
                try:
                    subprocess.run(['python', 'manage.py', 'loaddata', fixture_file], check=True)
                except subprocess.CalledProcessError as e:
                    pass
        
        except Exception as e:
            print(f"Ocurrió un error al intentar cargar los fixtures para la aplicación {app}: {e}")


if __name__ == "__main__":
    # Crear el superusuario
    crear_superusuario()

    # Cargar los fixtures
    cargar_todos_los_fixtures()
