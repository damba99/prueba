from django.shortcuts import render, get_object_or_404, redirect
from .models import Sesion, Clase, Disciplina, Categoria
from profesores.models import Profesor

# Listado de sesiones
def listar_sesiones(request):
    sesiones = Sesion.objects.all()
    return render(request, 'listar_sesiones.html', {'sesiones': sesiones})

# Crear sesión
def crear_sesion(request):
    if request.method == 'POST':
        id_clase = request.POST.get('id_clase')
        id_profesor = request.POST.get('id_profesor')
        dia = request.POST.get('dia')
        turno = request.POST.get('turno')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')

        clase = get_object_or_404(Clase, pk=id_clase)
        profesor = get_object_or_404(Profesor, pk=id_profesor)

        sesion = Sesion(
            id_clase=clase,
            id_profesor=profesor,
            dia=dia,
            turno=turno,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        sesion.save()
        return redirect('listar_sesiones')
    
    clases = Clase.objects.all()
    profesores = Profesor.objects.all()
    return render(request, 'crear_sesion.html', {'clases': clases, 'profesores': profesores})

# Modificar sesión
def modificar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)

    if request.method == 'POST':
        sesion.id_clase = get_object_or_404(Clase, pk=request.POST.get('id_clase'))
        sesion.id_profesor = get_object_or_404(Profesor, pk=request.POST.get('id_profesor'))
        sesion.dia = request.POST.get('dia')
        sesion.turno = request.POST.get('turno')
        sesion.hora_inicio = request.POST.get('hora_inicio')
        sesion.hora_fin = request.POST.get('hora_fin')
        sesion.save()
        return redirect('detalle_sesion', pk=sesion.pk)
    
    clases = Clase.objects.all()
    profesores = Profesor.objects.all()
    return render(request, 'modificar_sesion.html', {'sesion': sesion, 'clases': clases, 'profesores': profesores})

# Eliminar sesión
def eliminar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)

    if request.method == 'POST':
        sesion.delete()
        return redirect('listar_sesiones')
    
    return render(request, 'eliminar_sesion.html', {'sesion': sesion})

# Detalle de sesión
def detalle_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)
    return render(request, 'detalle_sesion.html', {'sesion': sesion})

# Listado de clases
def listar_clases(request):
    clases = Clase.objects.all()
    return render(request, 'listar_clases.html', {'clases': clases})

# Crear clase
def crear_clase(request):
    if request.method == 'POST':
        id_disciplina = request.POST.get('id_disciplina')
        id_categoria = request.POST.get('id_categoria')
        print("disciplina", id_disciplina)
        print("cat ", id_categoria)

        if not id_disciplina or not id_categoria:
            # Puedes agregar un mensaje de error si es necesario
            return render(request, 'crear_clase.html', {
                'disciplinas': Disciplina.objects.all(),
                'categorias': Categoria.objects.all(),
                'error_message': 'Debe seleccionar una disciplina y una categoría.'
            })

        # Asegurarse de que el id_disciplina y el id_categoria son válidos
        disciplina = get_object_or_404(Disciplina, pk=id_disciplina)
        categoria = get_object_or_404(Categoria, pk=id_categoria)
        
        # Crear la clase
        clase = Clase(id_disciplina=disciplina, id_categoria=categoria)
        clase.save()
        
        return redirect('listar_clases')

    disciplinas = Disciplina.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'crear_clase.html', {'disciplinas': disciplinas, 'categorias': categorias})

# Modificar clase
def modificar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)

    if request.method == 'POST':
        clase.nombre = request.POST.get('nombre')
        clase.id_disciplina = get_object_or_404(Disciplina, pk=request.POST.get('id_disciplina'))
        clase.id_categoria = get_object_or_404(Categoria, pk=request.POST.get('id_categoria'))
        clase.save()
        return redirect('detalle_clase', pk=clase.pk)

    disciplinas = Disciplina.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'modificar_clase.html', {'clase': clase, 'disciplinas': disciplinas, 'categorias': categorias})

# Eliminar clase
def eliminar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)

    if request.method == 'POST':
        clase.delete()
        return redirect('listar_clases')
    
    return render(request, 'eliminar_clase.html', {'clase': clase})

# Detalle de clase
def detalle_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    return render(request, 'detalle_clase.html', {'clase': clase})
