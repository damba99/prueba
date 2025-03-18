from django.shortcuts import render, get_object_or_404, redirect
from .models import Cuota
import datetime
from datetime import date
from alumnos.models import AlumnoClase, Alumno  
from cuotas.models import Monto, Periodo, Inscripcion

def crear_cuotas():
    alumnos = AlumnoClase.objects.all()
    mes_actual = datetime.datetime.now().month
    anio_actual = datetime.datetime.now().year
    for objeto in alumnos:
        
        for mes in range(mes_actual, 13):
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

def listar_cuotas(request):
    cuotas = Cuota.objects.all()  
    crear_cuotas()
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
        cuota.monto = request.POST.get('monto', cuota.monto)  # Si no se envía, dejamos el valor actual
        cuota.fecha_pago = request.POST.get('fecha_pago', cuota.fecha_pago)
        cuota.estado = request.POST.get('estado', cuota.estado)
        cuota.fecha_vencimiento = request.POST.get('fecha_vencimiento', cuota.fecha_vencimiento)

        # Si hay un periodo y detalle, también los actualizamos
        periodo_id = request.POST.get('id_periodo')
        if periodo_id:
            cuota.id_periodo = Periodo.objects.get(id=periodo_id)

        detalle_id = request.POST.get('detalle')
        if detalle_id:
            cuota.detalle = AlumnoClase.objects.get(id=detalle_id)

        # Calculamos la fecha de vencimiento si es necesario
        cuota.clean()  # Ejecutamos la validación de estado
        cuota.save()  # Guardamos los cambios en la base de datos

        return redirect('listar_cuotas')  # Redirigimos a donde queramos después de guardar

    return render(request, 'modificar_cuota.html', {'cuota': cuota})