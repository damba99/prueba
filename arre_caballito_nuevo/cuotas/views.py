from django.shortcuts import render, get_object_or_404, redirect
from .models import Cuota
import datetime
from django.utils import timezone
from datetime import date
from alumnos.models import AlumnoClase, Alumno  
from cuotas.models import Monto, Periodo, Inscripcion

def crear_cuotas():
    alumnos = AlumnoClase.objects.all()
    mes_actual = datetime.datetime.now().month
    anio_actual = datetime.datetime.now().year
    for objeto in alumnos:
        inscripcion = Inscripcion.objects.filter(alumno=objeto.alumno, detalle=objeto.clase).first()
        if inscripcion and inscripcion.estado == 'pagado':
            for mes in range(mes_actual+1, 13):
                alumno = objeto
                a = f"{mes:02}"
                id_periodo = Periodo.objects.filter(mes=a, anio=anio_actual).first()
                monto = Monto.objects.filter(disciplina=objeto.clase.id_disciplina).first()
                monto = monto.monto
                anio_actual = int(anio_actual)
                mes = int(mes)
                fecha_vencimiento = date(anio_actual, mes, 10)
                detalle = objeto
                if not Cuota.objects.filter(alumno=alumno, detalle=detalle, id_periodo=id_periodo).exists():
                    cuota = Cuota(alumno=alumno, id_periodo=id_periodo, monto=monto, fecha_vencimiento= fecha_vencimiento, detalle=detalle)
                    cuota.save()

def actualizar_estado_todas_las_cuotas():
    cuotas_a_actualizar = Cuota.objects.all()
    current_date = timezone.now().date()

    for cuota in cuotas_a_actualizar:


        if cuota.estado != 'pagado' and cuota.estado != 'cancelada':
            print(cuota.estado)
            print(current_date, cuota.fecha_vencimiento)

            if current_date > cuota.fecha_vencimiento:
                print("Hola")
                cuota.estado = 'vencida'
            elif current_date < cuota.fecha_vencimiento:
                if cuota.fecha_vencimiento.year > current_date.year or (cuota.fecha_vencimiento.year == current_date.year and cuota.fecha_vencimiento.month > current_date.month):
                    cuota.estado = 'proximo'
                else:
                    cuota.estado = 'pendiente'
                print("picha")

        cuota.save()

def listar_cuotas(request):
    cuotas = Cuota.objects.all()  
    crear_cuotas()
    actualizar_estado_todas_las_cuotas()
    return render(request, 'listar_cuotas.html', {'cuotas': cuotas})

def listar_montos(request):
    montos = Monto.objects.all()
    return render(request, 'listar_montos.html', {'montos': montos})

def modificar_monto(request, pk):
    monto = Monto.objects.get(pk=pk)
    if request.method == 'POST':
        monto.monto = request.POST.get('monto')
        monto.save()
        cuotas = Cuota.objects.filter(estado='proximo')
        lista = []
        nuevo_monto = monto.monto
        for cuota in cuotas:

            if cuota.detalle.clase.id_disciplina == monto.disciplina:
                print(cuota.estado)
                print(cuota.detalle.clase.id_disciplina)
                cuota.monto = nuevo_monto
                cuota.clean()
                cuota.save()
        return redirect('listar_montos')
    return render(request, 'modificar_monto.html', {'monto': monto})

def modificar_cuota(request, pk):
    cuota = get_object_or_404(Cuota, id_cuota=pk)  # Obtener la cuota a modificar
    
    if request.method == 'POST':
        # Recibimos los valores de los campos del formulario
        cuota.estado = request.POST.get('estado', cuota.estado)

        # Calculamos la fecha de vencimiento si es necesario
        cuota.clean()  # Ejecutamos la validación de estado
        cuota.save()  # Guardamos los cambios en la base de datos

        return redirect('listar_cuotas')  # Redirigimos a donde queramos después de guardar

    return render(request, 'modificar_cuota.html', {'cuota': cuota})

def cuotas(request):
    alumnos = Alumno.objects.filter(id_alumno__in=AlumnoClase.objects.values('alumno'))
    return render(request, 'cuotas.html', {'alumnos': alumnos})

def deudas(request, pk):
    alumno = Alumno.objects.get(id_alumno=pk)
    print(alumno.id_alumno)
    alumno_clases = AlumnoClase.objects.filter(alumno=alumno).first()
    if not alumno_clases:
        print("El alumno no tiene clases asignadas.")
    cuotas = Cuota.objects.filter(alumno=alumno_clases)
    inscripciones = Inscripcion.objects.filter(alumno=alumno, estado='pendiente')
    conceptos = []
    crear_cuotas()
    for cuota in cuotas:
        print("a")
        conceptos.append({
            'tipo': 'cuota',
            'descripcion': f'Cuota {cuota.id_cuota} - {cuota.id_periodo}',
            'monto': cuota.monto,
            'estado': cuota.estado,
            'fecha_vencimiento': cuota.fecha_vencimiento
        })

    for inscripcion in inscripciones:
        conceptos.append({
            'tipo': 'inscripcion',
            'descripcion': f'Inscripción en {inscripcion.detalle.nombre}',
            'monto': inscripcion.monto, 
            'estado': inscripcion.estado, 
            'fecha_vencimiento': ""
  
        })
        
    return render(request, 'deudas.html', {'conceptos': conceptos, 'alumno': alumno})


    