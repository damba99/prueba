from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from alumnos.models import Alumno, AlumnoClase
def perfil(request, id):
    usuario = get_object_or_404(User, pk=id)
    alumno = get_object_or_404(Alumno, usuario=usuario)
    print(alumno)
    return render(request, 'perfil.html', {
        'user': usuario,
        'alumno': alumno,
        })

def perfilll(request, id):
    alumno = get_object_or_404(Alumno, usuario_id=id)
    clases = AlumnoClase.objects.filter(alumno=alumno, activo=True)
    clases_inscritas = [ac.clase for ac in clases]

    return render(request, 'perfil.html', {
        'usuario': request.user,
        'alumno': alumno,
        'clases': clases_inscritas
    })