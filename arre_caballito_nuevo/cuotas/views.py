from django.shortcuts import render
from .models import Cuota
import datetime
from datetime import date
from alumnos.models import AlumnoClase  
from cuotas.models import Monto, Periodo

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
            anio_actual = int(anio_actual)
            mes = int(mes)
            fecha_vencimiento = date(anio_actual, mes, 10)
            detalle = objeto
            print(type(fecha_vencimiento))
            print(type(mes))
            
            cuota = Cuota(alumno=alumno, id_periodo=id_periodo, monto=monto, fecha_vencimiento= fecha_vencimiento, detalle=detalle)
            cuota.save()

def listar_cuotas(request):
    cuotas = Cuota.objects.all()  
    crear_cuotas()
    return render(request, 'listar_cuotas.html', {'cuotas': cuotas})

