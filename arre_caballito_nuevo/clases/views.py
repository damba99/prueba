
from .models import Sesion, Clase, Disciplina, Categoria
from profesores.models import Profesor
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from alumnos.models import Asistencia, Alumno

# Listar todas las sesiones
def listar_sesiones(request):
    sesiones = Sesion.objects.all()
    return render(request, 'listar_sesiones.html', {'sesiones': sesiones})

# Crear una nueva sesión (usando request.POST.get)
def crear_sesion(request):
    if request.method == 'POST':
        id_profesor = request.POST.get('id_profesor')
        dia = request.POST.get('dia')
        id_clase = request.POST.get('id_clase')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        
        # Verificar que los datos son correctos antes de crear la sesión
        if id_profesor and dia and id_clase and hora_inicio and hora_fin:
            try:
                profesor = Profesor.objects.get(id_profesor=id_profesor)
                clase = Clase.objects.get(id_clase=id_clase)
                
                
                # Crear la sesión
                sesion = Sesion.objects.create(
                    id_profesor=profesor,
                    dia=dia,
                    id_clase=clase,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin
                )
                sesion.save()
                return redirect('listar_sesiones')
            except Profesor.DoesNotExist:
                return HttpResponse("Profesor no encontrado", status=404)
            except Clase.DoesNotExist:
                return HttpResponse("Clase no encontrada", status=404)
        else:
            print(id_profesor, id_clase, hora_inicio, hora_fin, dia)
            return HttpResponse("Los datos proporcionados no son válidos", status=400)
    
    # Obtener los profesores y clases para el formulario
    profesores = Profesor.objects.all()
    clases = Clase.objects.all()
    return render(request, 'crear_sesion.html', {'profesores': profesores, 'clases': clases})

# Modificar una sesión existente (usando request.POST.get)
def modificar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, id_sesion=pk)
    
    if request.method == 'POST':
        id_profesor = request.POST.get('id_profesor')
        dia = request.POST.get('dia')
        id_clase = request.POST.get('id_clase')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')

        # Actualizar los campos solo si se pasan nuevos datos
        if id_profesor:
            sesion.id_profesor = Profesor.objects.get(id=id_profesor)
        if dia:
            sesion.dia = dia
        if id_clase:
            sesion.id_clase = Clase.objects.get(id=id_clase)
        if hora_inicio:
            sesion.hora_inicio = hora_inicio
        if hora_fin:
            sesion.hora_fin = hora_fin
        
        sesion.save()
        return redirect('listar_sesiones')
    
    profesores = Profesor.objects.all()
    clases = Clase.objects.all()
    return render(request, 'modificar_sesion.html', {'sesion': sesion, 'profesores': profesores, 'clases': clases})

# Ver detalles de una sesión
def detalle_sesion(request, pk):
    sesion = get_object_or_404(Sesion, id_sesion=pk)
    return render(request, 'detalle_sesion.html', {'sesion': sesion})

# Eliminar una sesión
def eliminar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, id_sesion=pk)
    if request.method == 'POST':
        sesion.delete()
        return redirect('listar_sesiones')
    return render(request, 'eliminar_sesion.html', {'sesion': sesion})

# Listado de clases
def listar_clases(request):
    clases = Clase.objects.all()
    return render(request, 'listar_clases.html', {'clases': clases})

# Crear clase
def crear_clase(request):
    if request.method == 'POST':
        # Obtener los valores de id_disciplina y id_categoria desde el formulario
        id_disciplina = request.POST.get('id_disciplina')
        id_categoria = request.POST.get('id_categoria')

        # Validar si ambos campos fueron proporcionados
        if not id_disciplina or not id_categoria:
            return render(request, 'crear_clase.html', {
                'disciplinas': Disciplina.objects.all(),
                'categorias': Categoria.objects.all(),
                'error_message': 'Debe seleccionar una disciplina y una categoría.'
            })

        # Asegurarse de que id_disciplina y id_categoria son válidos
        disciplina = get_object_or_404(Disciplina, pk=id_disciplina)
        categoria = get_object_or_404(Categoria, pk=id_categoria)

        # Contar cuántas clases existen para esa combinación de disciplina y categoría
        clases = Clase.objects.all()
        cont = clases.count() + 1  # El contador será el número de clases + 1 para la nueva clase

        # Crear el nombre de la clase
        nombre = f"Grupo {cont} ({categoria.nombre})"

        # Crear la clase con el nombre generado y los objetos disciplina y categoria
        clase = Clase(nombre=nombre, id_disciplina=disciplina, id_categoria=categoria)
        clase.save()

        # Redirigir a la lista de clases
        return redirect('listar_clases')

    # Obtener todas las disciplinas y categorias para mostrarlas en el formulario
    disciplinas = Disciplina.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'crear_clase.html', {'disciplinas': disciplinas, 'categorias': categorias})

# Modificar clase
def modificar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)

    if request.method == 'POST':
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

from django.shortcuts import render
from django.core.serializers import serialize
from .models import Clase, Sesion

def datos_horario():
    clases = Clase.objects.filter(activo=True)
    sesiones = Sesion.objects.all()
    profesores = Profesor.objects.all()
    
    # Serializamos los QuerySets a formato JSON
    clases_json = serialize('json', clases)
    sesiones_json = serialize('json', sesiones)
    profesores_json = serialize('json', profesores)    
    # Pasamos los datos serializados al contexto
    context = {
        'clases_json': clases_json,
        'sesiones_json': sesiones_json,
        'profesores_json': profesores_json
    }
    return context

def horarios(request):
    context = datos_horario()
    return render(request, 'horarios.html', context)

def agregar_clase(request):
    if request.method == 'POST':
        # Obtener los valores de id_disciplina y id_categoria desde el formulario
        id_disciplina = request.POST.get('id_disciplina')
        id_categoria = request.POST.get('id_categoria')

        # Validar si ambos campos fueron proporcionados
        if not id_disciplina or not id_categoria:
            return render(request, 'crear_clase.html', {
                'disciplinas': Disciplina.objects.all(),
                'categorias': Categoria.objects.all(),
                'error_message': 'Debe seleccionar una disciplina y una categoría.'
            })

        # Asegurarse de que id_disciplina y id_categoria son válidos
        disciplina = get_object_or_404(Disciplina, pk=id_disciplina)
        categoria = get_object_or_404(Categoria, pk=id_categoria)

        # Contar cuántas clases existen para esa combinación de disciplina y categoría
        clases = Clase.objects.all()
        cont = clases.count() + 1  
        # Crear el nombre de la clase
        nombre = f"Categoria {categoria.nombre} ({disciplina.nombre})"

        # Crear la clase con el nombre generado y los objetos disciplina y categoria
        clase = Clase(nombre=nombre, id_disciplina=disciplina, id_categoria=categoria)
        clase.save()
        print(clase.nombre, clase.id_categoria, clase.id_disciplina)
        dias = dias = request.POST.getlist('dia')
        horas_inicio = request.POST.getlist('hora_inicio')
        horas_fin = request.POST.getlist('hora_fin')
        ids_profesor = request.POST.getlist('id_profesor')
        print(clase.id_clase)
        a = len(ids_profesor)
        print(a)
        profesores = []
        for ids in ids_profesor:
            profesor = get_object_or_404(Profesor, pk=ids)
            profesores.append(profesor)
            
        for dia, hora_inicio, hora_fin, profesor in zip(dias, horas_inicio, horas_fin, profesores):
            

            Sesion.objects.create(id_clase=clase, dia=dia, hora_inicio=hora_inicio, hora_fin=hora_fin, id_profesor=profesor)
            print(f"Clase: {clase.id_clase}, dia: {dia}, Inicio: {hora_inicio}, fin: {hora_fin}, profesor: {profesor}")
        return redirect('agregar_clase')

    context = datos_horario()
    disciplinas = Disciplina.objects.all()
    categorias = Categoria.objects.all()
    profesores = Profesor.objects.all()

    return render(request, 'agregar_clase.html', {
        **context,  # Incluir los datos de horarios en el contexto
        'disciplinas': disciplinas,
        'categorias': categorias,
        'profesores': profesores
    })
from alumnos.views import Alumno, AlumnoClase
from datetime import date

from collections import OrderedDict

def detalle_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)

    # Crear asistencias si es necesario
    crear_asistencias(clase)

    # Obtener los alumnos y sus asistencias
    alumnoxclase = AlumnoClase.objects.filter(clase=clase)
    alumnos = Alumno.objects.filter(id_alumno__in=[alumno.alumno.id_alumno for alumno in alumnoxclase]).order_by('apellido', 'nombre')
    sesiones = Sesion.objects.filter(id_clase=clase)
    asistencias = Asistencia.objects.filter(id_sesion__in=sesiones)

    hoy = date.today()

    # Separar futuras y pasadas
    futuras = sorted([a.fecha for a in asistencias if a.fecha >= hoy])
    pasadas = sorted([a.fecha for a in asistencias if a.fecha < hoy], reverse=True)

    # Tomar 1 futura (la más próxima) y hasta 4 pasadas
    fechas_seleccionadas = sorted(pasadas[:4] + futuras[:1])  # orden ascendente: más viejas a la derecha
    fechas_seleccionadas = list(OrderedDict.fromkeys(fechas_seleccionadas))

    # Obtener todas las asistencias necesarias para los alumnos y las fechas seleccionadas
    asistencias_filtradas = Asistencia.objects.filter(id_alumno__in=[alumno.id_alumno for alumno in alumnos], fecha__in=fechas_seleccionadas)

    return render(request, 'detalle_clase.html', {
        'clase': clase,
        'alumnos': alumnos,
        'fechas': fechas_seleccionadas,
        'asistencias': asistencias_filtradas,  # Pasamos las asistencias filtradas
        'sesiones': sesiones,
    })

    
""""""""""""""""""""""""""""""""""""""""""""""""""""""
def obtener_fecha_dia_sesion(dia_sesion):
    import datetime

    dias_semana = {
        'lunes': 0,
        'martes': 1,
        'miércoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sábado': 5,
        'domingo': 6
    }

    hoy = datetime.date.today()
    dia_actual = hoy.weekday()  # 0 = lunes, ..., 6 = domingo

    dia_sesion_numero = dias_semana.get(dia_sesion.lower())
    if dia_sesion_numero is None:
        raise ValueError(f'Día inválido: {dia_sesion}')

    dias_hasta_proximo = (dia_sesion_numero - dia_actual + 7) % 7
    dias_hasta_proximo = dias_hasta_proximo or 7  # Si es hoy, ir al mismo día pero la próxima semana

    fecha_sesion = hoy + datetime.timedelta(days=dias_hasta_proximo)
    return fecha_sesion


from datetime import date

def crear_asistencias(clase):
    from datetime import timedelta

    alumnos = AlumnoClase.objects.filter(clase=clase).values_list('alumno', flat=True)
    sesiones = Sesion.objects.filter(id_clase=clase)

    hoy = date.today()

    for sesion in sesiones:
        fecha_programada = obtener_fecha_dia_sesion(sesion.dia)  # Fecha correspondiente al día de la sesión esta semana

        for alumno_id in alumnos:
            alumno = Alumno.objects.filter(id_alumno=alumno_id).first()

            # Verifica si ya existe una asistencia futura (a partir de hoy) para ese alumno y sesión
            existe_futura = Asistencia.objects.filter(
                id_sesion=sesion,
                id_alumno=alumno,
                fecha__gte=fecha_programada
            ).exists()
            print(sesion, alumno, hoy)
            print(fecha_programada)
            if not existe_futura:
                # Crea la asistencia en la fecha que le corresponde esta semana
                Asistencia.objects.create(
                    id_alumno=alumno,
                    id_sesion=sesion,
                    fecha=fecha_programada,
                    estado='pendiente'
                )
                print("se ha creado a tu señora")


from caballos.models import Caballo
from datetime import datetime
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.http import HttpResponseRedirect


def marcar_asistencia(request, clase_id, fecha):
    clase = get_object_or_404(Clase, id_clase=clase_id)
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()

    alumnos = Alumno.objects.filter(id_alumno__in=[ac.alumno.id_alumno for ac in AlumnoClase.objects.filter(clase=clase)]) 

    asistencias = Asistencia.objects.filter(id_alumno__in=[alumno.id_alumno for alumno in alumnos], fecha=fecha_obj).order_by('id_alumno__apellido')

    asistencias_dict = {}
    for asistencia in asistencias:
        alumno_id = asistencia.id_alumno
        asistencias_dict[alumno_id] = {
            'estado': asistencia.estado,
            'caballo': asistencia.id_caballo,
            'id': asistencia.id,
            'fecha': asistencia.fecha
        }

    caballos = Caballo.objects.all()

    if request.method == 'POST':
        for alumno in alumnos:
            # Obtener los valores del formulario usando el id del alumno
            estado = request.POST.get(f'estado_{alumno.id_alumno}')
            caballo_id = request.POST.get(f'caballo_{alumno.id_alumno}')

            asistencia = Asistencia.objects.filter(id_alumno=alumno, fecha=fecha_obj).first()
            if asistencia:
                asistencia.estado = estado
                if caballo_id:
                    asistencia.id_caballo = Caballo.objects.get(id_caballo=caballo_id)
                asistencia.save()

        return HttpResponseRedirect(reverse('detalle_clase', args=[clase_id]))

    return render(request, 'marcar_asistencia.html', {
        'clase': clase,
        'alumnos': alumnos,
        'asistencias': asistencias_dict,
        'caballos': caballos,
        'fecha': fecha_obj,
    })

