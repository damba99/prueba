from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Caja, Movimiento
from django.contrib import messages
from decimal import Decimal



@login_required
def apertura_caja(request):
    if request.method == 'POST':
        monto_inicial = request.POST.get('monto_inicial')

        if monto_inicial:
            try:
                monto_inicial = Decimal(monto_inicial)

                caja = Caja.objects.create(
                    usuario_apertura=request.user,
                    fecha_apertura=timezone.now(),
                    monto_inicial=monto_inicial,
                    monto_final=0,
                    ingresos=0,
                    egresos=0,
                    estado=Caja.ABIERTO
                )

                return redirect('detalle_caja', pk=caja.pk)

            except Exception as e:
                return render(request, 'apertura_caja.html', {'error': f'Error al crear la caja: {e}'})
        else:
            return render(request, 'apertura_caja.html', {'error': 'Debe ingresar un monto inicial válido'})

    return render(request, 'apertura_caja.html')

def detalle_caja(request, pk):
    # Obtener el objeto Caja correspondiente al pk
    caja = get_object_or_404(Caja, pk=pk)

    # Renderizar el template con los detalles de la caja
    return render(request, 'detalle_caja.html', {'caja': caja})

@login_required
def cerrar_caja(request, pk):
    caja = get_object_or_404(Caja, pk=pk)

    if caja.estado == Caja.ABIERTO:
        # Actualizar ingresos y egresos antes de calcular saldo
        caja.actualizar_saldos()

        caja.estado = Caja.CERRADO
        caja.fecha_cierre = timezone.now()
        caja.usuario_cierre = request.user

        # Calcular el monto final usando la propiedad saldo (sin asignar saldo)
        caja.monto_final = caja.saldo

        caja.save()

    return redirect('detalle_caja', pk=caja.pk)

def listar_cajas(request):
    cajas = Caja.objects.all()
    caja_abierta = Caja.objects.filter(estado='Abierta').first()
    return render(request, 'listar_cajas.html', {'cajas': cajas, 'caja_abierta': caja_abierta})

@login_required
def registrar_movimiento(request):
    # Filtramos las cajas que están abiertas
    caja_abierta = Caja.objects.filter(estado=Caja.ABIERTO).first()

    # Si no hay una caja abierta, mostramos un mensaje de error
    if not caja_abierta:
        messages.error(request, 'No hay cajas abiertas. No se puede registrar un movimiento.')
        return redirect('listar_cajas')  # Redirige al listado de cajas

    if request.method == 'POST':
        # Recogemos los datos del formulario
        tipo = request.POST.get('tipo')
        monto = request.POST.get('monto')
        descripcion = request.POST.get('descripcion')

        # Convertimos el monto a Decimal
        try:
            monto_decimal = Decimal(monto)
        except:
            messages.error(request, 'Monto no válido.')
            return redirect('registrar_movimiento')

        # Validamos el tipo de movimiento
        if tipo not in ['Ingreso', 'Egreso']:
            messages.error(request, 'Tipo de movimiento no válido.')
            return redirect('registrar_movimiento')

        # Creamos el nuevo movimiento
        movimiento = Movimiento(
            id_caja=caja_abierta,
            descripcion = descripcion,
            fecha_y_hora=timezone.now(),
            tipo=tipo,
            monto=monto_decimal,
            usuario=request.user
        )

        # Guardamos el movimiento y la caja
        caja_abierta.save()
        movimiento.save()

        messages.success(request, f'Movimiento registrado correctamente: {tipo} de ${monto_decimal}.')
        return redirect('detalle_caja', pk=caja_abierta.pk)

    return render(request, 'registrar_movimiento.html', {'caja': caja_abierta})

def movimientos_caja(request, pk):
    # Obtén la caja con el id proporcionado
    caja = Caja.objects.get(pk=pk)

    # Obtén todos los movimientos relacionados con esta caja
    movimientos = Movimiento.objects.filter(id_caja=caja)

    return render(request, 'movimientos_caja.html', {'caja': caja, 'movimientos': movimientos})

# views.py
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from .models import Movimiento
from decimal import Decimal
from datetime import timedelta

def dashboard(request):
    # Obtener el período (por defecto será 'diario')
    periodo = request.GET.get('periodo', 'diario')
    current_date = timezone.now().date()

    # Datos de ingresos y egresos
    data_ingresos = []
    data_egresos = []
    labels = []

    if periodo == 'diario':
        # Últimos 30 días
        for i in range(30):
            day = current_date - timedelta(days=i)
            labels.append(day.strftime('%d-%m-%Y'))
            ingresos = Movimiento.objects.filter(fecha_y_hora__date=day, tipo='Ingreso').aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            egresos = Movimiento.objects.filter(fecha_y_hora__date=day, tipo='Egreso').aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            data_ingresos.append(ingresos)
            data_egresos.append(egresos)

    elif periodo == 'semanal':
        # Últimos 4 semanas
        for i in range(4):
            start_of_week = current_date - timedelta(weeks=i)
            labels.append(start_of_week.strftime('%d-%m-%Y'))
            ingresos = Movimiento.objects.filter(fecha_y_hora__date__week=start_of_week.week, tipo='Ingreso').aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            egresos = Movimiento.objects.filter(fecha_y_hora__date__week=start_of_week.week, tipo='Egreso').aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            data_ingresos.append(ingresos)
            data_egresos.append(egresos)

    # Similar para los otros periodos (mensual y anual)

    # Enviar los datos a la plantilla
    return render(request, 'dashboard.html', {
        'labels': labels,
        'data_ingresos': data_ingresos,
        'data_egresos': data_egresos,
    })
