from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from alumnos.models import Alumno, AlumnoClase
from .models import Perfil
from django.contrib.auth.decorators import login_required

def crear_perfil(usuario):
    perfil= Perfil.objects.get_or_create(usuario=usuario)
    return perfil

def perfil(request, id):
    usuario = get_object_or_404(User, pk=id)
    crear_perfil(usuario)
    alumno = get_object_or_404(Alumno, usuario=usuario)
    perfil = Perfil.objects.get(usuario=usuario)  # Obtener el perfil del usuario

    return render(request, 'perfil.html', {
        'user': usuario,
        'alumno': alumno,
        'perfil': perfil,  # Pasar el perfil al template
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
    
@login_required
def actualizar_foto_perfil(request, id=None):
    usuario = request.user

    # Si es admin y se especifica ID, puede modificar cualquier perfil
    if usuario.is_superuser and id:
        perfil = get_object_or_404(Perfil, usuario__id=id)
    else:
        # Si no es admin, siempre modifica su propio perfil
        perfil = get_object_or_404(Perfil, usuario=usuario)

    if request.method == "POST" and request.FILES.get('foto_perfil'):
        perfil.foto_perfil = request.FILES['foto_perfil']
        perfil.save()
        return redirect('perfil', id=perfil.usuario.id)

    return render(request, 'actualizar_foto_perfil.html', {'perfil': perfil})