# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Caballo, CaballoDisciplina
from clases.models import Disciplina

# Vista para crear un caballo
def crear_caballo(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        edad = request.POST.get("edad")
        sexo = request.POST.get("sexo")

        # Crear el caballo
        caballo = Caballo.objects.create(
            nombre=nombre,
            edad=edad,
            sexo=sexo
        )

        # Asociar disciplinas si se seleccionan
        disciplinas_seleccionadas = request.POST.getlist("disciplinas")
        for disciplina_id in disciplinas_seleccionadas:
            disciplina = Disciplina.objects.get(id_disciplina=disciplina_id)
            CaballoDisciplina.objects.create(caballo=caballo, disciplina=disciplina)

        return redirect("listar_caballos")
    else:
        disciplinas = Disciplina.objects.all()
        return render(request, "crear_caballo.html", {"disciplinas": disciplinas})

# Vista para listar caballos
def listar_caballos(request):
    caballos = Caballo.objects.all()
    return render(request, "listar_caballos.html", {"caballos": caballos})

# Vista para modificar un caballo
from django.shortcuts import render, get_object_or_404, redirect
from .models import Caballo, CaballoDisciplina
from clases.models import Disciplina

def modificar_caballo(request, pk):
    # Obtener el objeto Caballo con el pk dado
    caballo = get_object_or_404(Caballo, pk=pk)
    disciplinas = Disciplina.objects.all()  # Obtener todas las disciplinas disponibles

    if request.method == "POST":
        # Actualizar los campos básicos del caballo
        caballo.nombre = request.POST.get("nombre")
        caballo.edad = request.POST.get("edad")
        caballo.sexo = request.POST.get("sexo")
        caballo.save()

        # Limpiar las disciplinas asociadas y asignar las nuevas seleccionadas
        CaballoDisciplina.objects.filter(caballo=caballo).delete()  # Eliminar las disciplinas previas

        # Obtener las disciplinas seleccionadas del formulario
        disciplinas_seleccionadas = request.POST.getlist("disciplinas")

        # Añadir las disciplinas seleccionadas al caballo
        for disciplina_id in disciplinas_seleccionadas:
            disciplina = Disciplina.objects.get(id_disciplina=disciplina_id)
            CaballoDisciplina.objects.create(caballo=caballo, disciplina=disciplina)

        # Redirigir a la página de detalles del caballo
        return redirect("detalle_caballo", pk=caballo.pk)

    return render(request, "modificar_caballo.html", {"caballo": caballo, "disciplinas": disciplinas})

# Vista para eliminar un caballo
def eliminar_caballo(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)

    if request.method == "POST":
        caballo.delete()
        return redirect("listar_caballos")

    return render(request, "eliminar_caballo.html", {"caballo": caballo})

# Vista para ver los detalles de un caballo
def detalle_caballo(request, pk):
    caballo = get_object_or_404(Caballo, pk=pk)
    disciplinas = CaballoDisciplina.objects.filter(caballo=caballo)
    return render(request, "detalle_caballo.html", {"caballo": caballo, "disciplinas": disciplinas})
