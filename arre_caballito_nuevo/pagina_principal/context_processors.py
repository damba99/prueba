# pagina_principal/context_processors.py

from django.contrib.auth.models import Group

def user_groups(request):
    """
    Agrega información sobre los grupos del usuario al contexto global
    """
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name="Admin").exists()
        is_profesor = request.user.groups.filter(name="Profesor").exists()
        is_alumno = request.user.groups.filter(name="Alumno").exists()
    else:
        is_admin = is_profesor = is_alumno = False

    return {
        'is_admin': is_admin,
        'is_profesor': is_profesor,
        'is_alumno': is_alumno
    }
