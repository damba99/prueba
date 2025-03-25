from django.shortcuts import render, get_object_or_404, redirect
from .models import Alumno, AlumnoClase
from .forms import AlumnoForm
from clases.models import Categoria
from cuotas.models import Inscripcion, Monto, Cuota

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
    clases = AlumnoClase.objects.filter(alumno=alumno, activo=True)
    
    clases_inscritas = [alumno_clase.clase for alumno_clase in clases]

    return render(request, 'detalle_alumno.html', {
        'alumno': alumno,
        'clases': clases_inscritas
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Alumno, Clase, AlumnoClase
from django.contrib import messages

def inscribir_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    clases_disponibles = Clase.objects.filter(id_categoria=alumno.id_categoria).exclude(
        id_clase__in=[
            alumno_clase.clase.id_clase
            for alumno_clase in alumno.clases.filter(activo=True)
        ]
    )

    if request.method == 'POST':
        clases_seleccionadas = request.POST.getlist('clases')

        for clase_id in clases_seleccionadas:
            clase = get_object_or_404(Clase, pk=clase_id)
            print("Clasesita")
            alumno_clase = AlumnoClase.objects.filter(alumno=alumno, clase=clase).first()
            print(alumno_clase)
            if alumno_clase:
                cuotas_canceladas = Cuota.objects.filter(alumno=alumno_clase, estado='cancelada')
                for cuota in cuotas_canceladas:
                    cuota.estado = 'pendiente'
                    cuota.save()
                alumno_clase.activo=True
                alumno_clase.save()
                for a in cuotas_canceladas:
                    print(a.estado)
            else:
                alumno_clase = AlumnoClase.objects.create(alumno=alumno, clase=clase)
                monto = Monto.objects.filter(disciplina=clase.id_disciplina.id_disciplina, tipo='inscripcion').first()
                if monto:
                    Inscripcion.objects.create(alumno=alumno, monto=monto, detalle=clase)

        messages.success(request, f"{alumno.nombre} {alumno.apellido} ha sido inscrito exitosamente en las clases seleccionadas.")
        
        return redirect('detalle_alumno', pk=alumno.pk)

    return render(request, 'inscribir_alumno.html', {
        'alumno': alumno,
        'clases': clases_disponibles
    })

    
def eliminar_inscripcion(request, alumno_pk, clase_pk):
        # Obtener al alumno y la clase usando sus pk
        alumno = get_object_or_404(Alumno, pk=alumno_pk)
        clase = get_object_or_404(Clase, pk=clase_pk)
        print("aaaaaaaaaaa")
        # Verificar si el alumno está inscrito en la clase
        inscripcion = AlumnoClase.objects.filter(alumno=alumno, clase=clase).first()
        cuotas = Cuota.objects.filter(alumno=inscripcion)
        
        if not inscripcion:
            messages.error(request, f"El alumno no está inscrito en la clase '{clase.nombre}'.")
            return redirect('detalle_alumno', pk=alumno.pk)
        
        # Si es un POST, eliminar la inscripción
        if request.method == 'POST':
            # Eliminar la relación AlumnoClase
            inscripcion.activo=False
            inscripcion.save()
            for cuota in cuotas:
                if cuota.estado != 'pagado':
                    print(cuota)
                    cuota.estado = 'cancelada'
                    cuota.clean()
                    cuota.save()
                    print(cuota)
            messages.success(request, f"Inscripción en la clase '{clase.nombre}' eliminada correctamente.")
            return redirect('detalle_alumno', pk=alumno.pk)
        
        # Si no es POST, mostrar la confirmación
        return render(request, 'eliminar_inscripcion.html', {
            'alumno': alumno,
            'clase': clase,
        })
