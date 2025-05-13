from django.shortcuts import render, redirect
from .models import Competencia, Evento
from django.http import HttpResponseBadRequest
from clases.models import Disciplina, Categoria
from django.shortcuts import render, get_object_or_404, redirect


def listar_competencias(request):
    competencias = Competencia.objects.all().order_by('fecha_hora')
    disciplinas = Disciplina.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'listar_competencias.html', {
        'competencias': competencias,
        'disciplinas': disciplinas,
        'categorias': categorias,
    })


def crear_competencia(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        lugar = request.POST.get('lugar')
        fecha_hora = request.POST.get('fecha_hora')

        if not nombre or not descripcion or not lugar or not fecha_hora:
            return HttpResponseBadRequest("Faltan datos en el formulario")

        # Crear y guardar la nueva competencia
        competencia = Competencia(
            nombre=nombre,
            descripcion=descripcion,
            lugar=lugar,
            fecha_hora=fecha_hora
        )
        competencia.save()
        return redirect('listar_competencias')  # Redirigir al listado de competencias después de guardar

    return HttpResponseBadRequest("Método no permitido")

def agregar_evento(request, id_competencia):
    if request.method == 'POST':
        competencia = get_object_or_404(Competencia, id_competencias=id_competencia)
        id_disciplina = request.POST.get('disciplina')
        id_categoria = request.POST.get('categoria')

        if not id_disciplina or not id_categoria:
            return HttpResponseBadRequest("Faltan datos")

        evento = Evento(
            id_competencia=competencia,
            id_disciplina_id=id_disciplina,
            id_categoria_id=id_categoria
        )
        evento.save()
        return redirect('listar_competencias')

    return HttpResponseBadRequest("Método no permitido")
    
def detalles_competencia(request, id_competencia):
    # Obtén la competencia especificada
    competencia = get_object_or_404(Competencia, id_competencias=id_competencia)
    
    # Obtener los eventos relacionados a esta competencia
    eventos = Evento.objects.filter(id_competencia=competencia)
    
    # Aquí, en lugar de redirigir, devolvemos un HTML para el modal
    if request.is_ajax():
        return render(request, 'detalles_competencia_modal.html', {
            'competencia': competencia,
            'eventos': eventos
        })

    # Si no es una solicitud AJAX, puedes redirigir al listado
    return redirect('listar_competencias')