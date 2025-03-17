from django.shortcuts import render, get_object_or_404, redirect
from .models import Profesor
from clases.models import Categoria

def crear_profesor(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        
        profesor = Profesor(
            nombre=nombre, apellido=apellido, dni=dni,
            fecha_nacimiento=fecha_nacimiento, direccion=direccion,
            telefono=telefono, email=email
        )
        profesor.save()
        return redirect('listar_profesores')
    
    return render(request, 'crear_profesor.html')

def listar_profesores(request):
    profesores = Profesor.objects.all()
    return render(request, 'listar_profesores.html', {'profesores': profesores})

def modificar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == "POST":
        profesor.nombre = request.POST.get('nombre')
        profesor.apellido = request.POST.get('apellido')
        profesor.dni = request.POST.get('dni')
        profesor.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        profesor.direccion = request.POST.get('direccion')
        profesor.telefono = request.POST.get('telefono')
        profesor.email = request.POST.get('email')
        profesor.save()
        return redirect('detalle_profesor', pk=profesor.pk)

    return render(request, 'modificar_profesor.html', {'profesor': profesor})

def eliminar_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    if request.method == "POST":
        profesor.delete()
        return redirect('listar_profesores')
    return render(request, 'eliminar_profesor.html', {'profesor': profesor})

def detalle_profesor(request, pk):
    profesor = get_object_or_404(Profesor, pk=pk)
    return render(request, 'detalle_profesor.html', {'profesor': profesor})
