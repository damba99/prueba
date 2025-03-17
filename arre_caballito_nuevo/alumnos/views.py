from django.shortcuts import render, get_object_or_404, redirect
from .models import Alumno
from .forms import AlumnoForm
from clases.models import Categoria

def crear_alumno(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        id_categoria = request.POST.get('id_categoria')
        
        alumno = Alumno(
            nombre=nombre, apellido=apellido, dni=dni,
            fecha_nacimiento=fecha_nacimiento, direccion=direccion,
            telefono=telefono, email=email, id_categoria_id=id_categoria
        )
        alumno.save()
        return redirect('listar_alumnos')
    
    categorias = Categoria.objects.all()  # Obtén las categorías disponibles
    return render(request, 'crear_alumno.html', {'categorias': categorias})

def listar_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'listar_alumnos.html', {'alumnos': alumnos})

def modificar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == "POST":
        alumno.nombre = request.POST.get('nombre')
        alumno.apellido = request.POST.get('apellido')
        alumno.dni = request.POST.get('dni')
        alumno.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        alumno.direccion = request.POST.get('direccion')
        alumno.telefono = request.POST.get('telefono')
        alumno.email = request.POST.get('email')
        alumno.id_categoria_id = request.POST.get('id_categoria')
        alumno.save()
        return redirect('detalle_alumno', pk=alumno.pk)

    categorias = Categoria.objects.all()
    return render(request, 'modificar_alumno.html', {'alumno': alumno, 'categorias': categorias})

def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == "POST":
        alumno.delete()
        return redirect('listar_alumnos')
    return render(request, 'eliminar_alumno.html', {'alumno': alumno})

def detalle_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    return render(request, 'detalle_alumno.html', {'alumno': alumno})
