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
    crear_cuotas()
    actualizar_estado_todas_las_cuotas()
    return render(request, 'cuotas.html', {'alumnos': alumnos})

from django.shortcuts import render, redirect
from .models import Cuota, Inscripcion, Alumno, AlumnoClase
from django.contrib import messages

def deudas(request, pk):
    alumno = Alumno.objects.get(id_alumno=pk)

    # Filtrar las cuotas no pagadas y no canceladas
    alumno_clases = AlumnoClase.objects.filter(alumno=alumno).first()
    if not alumno_clases:
        return render(request, 'deudas.html', {'conceptos': [], 'alumno': alumno})

    cuotas = Cuota.objects.filter(alumno=alumno_clases).exclude(estado='pagado').exclude(estado='cancelada')
    inscripciones = Inscripcion.objects.filter(alumno=alumno, estado='pendiente')

    conceptos = []
    
    # Añadir las cuotas a los conceptos
    for cuota in cuotas:
        conceptos.append({
            'id': cuota.id_cuota,
            'tipo': 'cuota',
            'descripcion': f'Cuota {cuota.id_cuota} - {cuota.id_periodo}',
            'monto': cuota.monto,
            'estado': cuota.estado,
            'fecha_vencimiento': cuota.fecha_vencimiento
        })

    # Añadir las inscripciones a los conceptos
    for inscripcion in inscripciones:
        conceptos.append({
            'id': inscripcion.pk,
            'tipo': 'inscripcion',
            'descripcion': f'Inscripción en {inscripcion.detalle.nombre}',
            'monto': inscripcion.monto.monto,
            'estado': inscripcion.estado,
            'fecha_vencimiento': ''
        })
    
    return render(request, 'deudas.html', {'conceptos': conceptos, 'alumno': alumno})

from django.contrib import messages
from cajas.models import Pago, Movimiento, Caja

def registrar_pago(request, pk):
    alumno = Alumno.objects.get(id_alumno=pk)

    if request.method == "POST":
        conceptos_seleccionados = request.POST.getlist('conceptos_seleccionados')
        conceptos_detalles = []
        total_monto = 0.0

        # Recorremos los conceptos seleccionados para procesarlos
        for concepto in conceptos_seleccionados:
            print(concepto)  # Esto mostrará el valor exacto de cada checkbox enviado
            try:
                # Dividimos la cadena recibida para obtener los detalles
                concepto_id, concepto_tipo, concepto_descripcion, concepto_monto, concepto_estado = concepto.split(';')
                concepto_monto = float(concepto_monto)  # Asegúrate de convertir el monto a float
                conceptos_detalles.append({
                    'id': concepto_id,
                    'tipo': concepto_tipo,
                    'descripcion': concepto_descripcion,
                    'monto': concepto_monto,
                    'estado': concepto_estado
                })
                total_monto += concepto_monto
            except ValueError:
                print(f"Error al dividir el concepto: {concepto}")

        # Pasar los detalles de los conceptos y el total a la plantilla
        return render(request, 'registrar_pago.html', {
            'alumno': alumno,
            'conceptos_detalles': conceptos_detalles,
            'total_monto': total_monto
        })

    # Si no es un POST, redirigir a la vista de deudas
    return redirect('deudas', pk=alumno.id_alumno)


def pago_a_movimiento(usuario, id_pago, monto):
    # Obtener la caja abierta (si existe)
    caja = Caja.objects.filter(estado='Abierta').first()  
    if not caja:
        
        print("No hay caja abierta")
        return None

   
    pago = Pago.objects.get(id_pagos=id_pago)

    print(caja)
    print(pago)
    movimiento = Movimiento.objects.create(
        id_caja=caja,
        tipo=Movimiento.INGRESO,
        fecha_y_hora = timezone.now(),
        monto=monto,
        id_pago=pago,  
        usuario=usuario  
    )
    caja.save()
    return movimiento

def pagar(request, pk):
    alumno = Alumno.objects.get(id_alumno=pk)

    if request.method == "POST":
        # Obtenemos la lista de los conceptos seleccionados
        conceptos_seleccionados = request.POST.getlist('conceptos_seleccionados')
        metodo_pago = request.POST.get('metodo_pago')  # Obtener el método de pago seleccionado
        conceptos_detalles = []
        total_monto = 0.0
        cuotas_a_pagar = []  # Lista para almacenar las cuotas asociadas al pago
        inscripcion_a_pagar = None  # Para almacenar la inscripción si corresponde

        # Recorremos los conceptos seleccionados para procesarlos
        for concepto in conceptos_seleccionados:
            print(concepto)
            try:
                # Dividimos la cadena recibida para obtener los detalles
                concepto_id, concepto_tipo, concepto_descripcion, concepto_monto, concepto_estado = concepto.split(';')
                concepto_monto = float(concepto_monto)  # Asegúrate de convertir el monto a float
                conceptos_detalles.append({
                    'id': concepto_id,
                    'tipo': concepto_tipo,
                    'descripcion': concepto_descripcion,
                    'monto': concepto_monto,
                    'estado': concepto_estado
                })
                total_monto += concepto_monto

                # Si es inscripción, la marcamos como pagada
                if concepto_tipo == 'inscripcion':
                    inscripcion_a_pagar = Inscripcion.objects.get(pk=concepto_id)
                    inscripcion_a_pagar.estado = 'pagado'  # Cambiar estado a 'pagado'
                    inscripcion_a_pagar.save()

                # Si es cuota, la marcamos como pagada
                if concepto_tipo == 'cuota':
                    cuota = Cuota.objects.get(pk=concepto_id)
                    cuotas_a_pagar.append(cuota)  # Añadir cuota a la lista de cuotas a pagar
                    cuota.estado = 'pagado'  # Cambiar estado a 'pagado'
                    cuota.save()

            except ValueError:
                print(f"Error al dividir el concepto: {concepto}")

        # Guardar el registro del pago con el método de pago y las cuotas/inscripción asociadas
        pago = Pago(
            monto=total_monto,
            medio_pago=metodo_pago  # Guardamos el método de pago seleccionado
        )
        pago.save()

        # Asociar las cuotas al pago
        if cuotas_a_pagar:
            pago.cuotas.set(cuotas_a_pagar)  # Asignar cuotas relacionadas al pago
            pago.save()
            
        # Si hay una inscripción, asociarla al pago
        if inscripcion_a_pagar:
            pago.inscripcion = inscripcion_a_pagar
            pago.save()  # Guardar el pago nuevamente para incluir la inscripción
        
        usuario = request.user 
        id_pago = pago.id_pagos
        pago_a_movimiento(usuario=usuario, id_pago=id_pago, monto=pago.monto)
        
        # Mostrar mensaje de éxito después de procesar el pago
        messages.success(request, "Pago registrado correctamente.")

        # Redirigir al usuario a la vista de deudas para este alumno
        return redirect('deudas', pk=alumno.id_alumno)

    # Si no es un POST, redirigir a la vista de deudas
    return redirect('deudas', pk=alumno.id_alumno)

from calendar import month_name
from django.db.models import Count


def grafico_cuotas(request):
    # Agrupar cuotas por mes y estado (solo pagadas y vencidas)
    cuotas_por_mes = (
        Cuota.objects
        .filter(estado__in=['pagado', 'vencida'])
        .values('id_periodo__mes', 'estado')
        .annotate(total=Count('id_cuota'))
        .order_by('id_periodo__mes')
    )

    # Crear estructura de datos
    meses = [str(i).zfill(2) for i in range(1, 13)]
    etiquetas = [month_name[int(m)] for m in meses]
    pagadas = []
    vencidas = []

    for mes in meses:
        total_pagadas = next((c['total'] for c in cuotas_por_mes if c['id_periodo__mes'] == mes and c['estado'] == 'pagado'), 0)
        total_vencidas = next((c['total'] for c in cuotas_por_mes if c['id_periodo__mes'] == mes and c['estado'] == 'vencida'), 0)
        pagadas.append(total_pagadas)
        vencidas.append(total_vencidas)

    return render(request, 'grafico_cuotas.html', {
        'etiquetas': etiquetas,
        'pagadas': pagadas,
        'vencidas': vencidas,
    })