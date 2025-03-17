from django.shortcuts import render, get_object_or_404, redirect
from .models import Caballo
from clases.models import Disciplina

# Vista para crear un nuevo caballo
def crear_caballo(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        disciplinas_ids = request.POST.getlist('disciplinas')

        caballo = Caballo(
            nombre=nombre, edad=edad, sexo=sexo
        )
        caballo.save()
        
        # Asignamos las disciplinas
        disciplinas = Disciplina.objects.filter(id__in=disciplinas_ids)
        caballo.disciplinas.set(disciplinas)
        caballo.save()

        return redirect('listar_caballos')

    disciplinas = Disciplina.objects.all()
    return render(request, 'crear_caballo.html', {'disciplinas': disciplinas})

# Vista para listar los caballos
def listar_caballos(request):
    caballos = Caballo.objects.all()
    return render(request, 'listar_caballos.html', {'caballos': caballos})

# Vista para modificar un caballo
def modificar_caballo(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    if request.method == "POST":
        caballo.nombre = request.POST.get('nombre')
        caballo.edad = request.POST.get('edad')
        caballo.sexo = request.POST.get('sexo')
        disciplinas_ids = request.POST.getlist('disciplinas')

        # Asignamos las disciplinas
        disciplinas = Disciplina.objects.filter(id__in=disciplinas_ids)
        caballo.disciplinas.set(disciplinas)
        caballo.save()

        return redirect('detalle_caballo', pk=caballo.pk)

    disciplinas = Disciplina.objects.all()
    return render(request, 'modificar_caballo.html', {'caballo': caballo, 'disciplinas': disciplinas})

# Vista para eliminar un caballo
def eliminar_caballo(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    if request.method == "POST":
        caballo.delete()
        return redirect('listar_caballos')
    return render(request, 'eliminar_caballo.html', {'caballo': caballo})

# Vista para mostrar los detalles de un caballo
def detalle_caballo(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    return render(request, 'detalle_caballo.html', {'caballo': caballo})
