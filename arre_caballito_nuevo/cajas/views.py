from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Caja, Movimiento
from django.contrib import messages
from decimal import Decimal



@login_required
def apertura_caja(request):
    if request.method == 'POST':
        # Obtener el monto inicial enviado en el POST
        monto_inicial = request.POST.get('monto_inicial')

        # Si el monto inicial es proporcionado y es un valor válido
        if monto_inicial and monto_inicial.isdigit():
            monto_inicial = float(monto_inicial)
            
            # Crear un objeto Caja nuevo con estado 'Abierta' y el usuario logueado
            caja = Caja.objects.create(
                usuario_apertura=request.user,
                fecha_apertura=timezone.now(),
                monto_inicial=monto_inicial,
                monto_final=0,  # El monto final será 0 al inicio
                ingresos=0,
                egresos=0,
                saldo=monto_inicial,  # Al inicio, el saldo es igual al monto inicial
                estado=Caja.ABIERTO  # El estado será 'Abierta'
            )

            # Redirigir a una vista de éxito o página que muestre la caja abierta
            return redirect('detalle_caja', pk=caja.pk)  # Suponiendo que tienes una vista para ver detalles de la caja abierta
        else:
            # Si el monto no es válido, mostrar un mensaje de error
            return render(request, 'apertura_caja.html', {'error': 'Debe ingresar un monto inicial válido'})
    
    # Si la petición es GET, mostrar el formulario para la apertura de caja
    return render(request, 'apertura_caja.html')

def detalle_caja(request, pk):
    # Obtener el objeto Caja correspondiente al pk
    caja = get_object_or_404(Caja, pk=pk)

    # Renderizar el template con los detalles de la caja
    return render(request, 'detalle_caja.html', {'caja': caja})

@login_required
def cerrar_caja(request, pk):
    # Obtener la caja correspondiente al pk
    caja = get_object_or_404(Caja, pk=pk)

    # Verificar si la caja está abierta
    if caja.estado == Caja.ABIERTO:
        # Cambiar el estado de la caja a cerrada
        caja.estado = Caja.CERRADO
        caja.fecha_cierre = timezone.now()
        caja.usuario_cierre = request.user
        
        # Aquí puedes calcular el monto final, saldo, etc., si es necesario
        caja.monto_final = caja.monto_inicial + caja.ingresos - caja.egresos
        caja.saldo = caja.monto_final
        
        # Guardar la caja con los nuevos datos
        caja.save()

    # Redirigir al detalle de la caja
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

