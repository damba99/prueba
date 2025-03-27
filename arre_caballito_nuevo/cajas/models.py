from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cuotas.models import Cuota, Inscripcion
from django.utils import timezone  # Para obtener la hora actual automáticamente

from django.db.models import Sum

class Caja(models.Model):
    ABIERTO = 'Abierta'
    CERRADO = 'Cerrada'
    ESTADO_CHOICES = [
        (ABIERTO, 'Abierta'),
        (CERRADO, 'Cerrada'),
    ]
    
    id_caja = models.AutoField(primary_key=True)
    usuario_apertura = models.ForeignKey(User, related_name='usuario_apertura', on_delete=models.CASCADE)
    usuario_cierre = models.ForeignKey(User, related_name='usuario_cierre', on_delete=models.CASCADE, null=True, blank=True)
    fecha_apertura = models.DateTimeField(default=timezone.now)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ingresos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    egresos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default=ABIERTO)

    @property
    def saldo(self):
        """Calcula el saldo como ingresos - egresos."""
        return (self.ingresos or 0) - (self.egresos or 0)

    def clean(self):
        if not self.usuario_apertura.groups.filter(name="Administrador").exists():
            raise ValidationError('El usuario de apertura debe ser un Administrador.')
        if not self.usuario_cierre.groups.filter(name="Administrador").exists():
            raise ValidationError('El usuario de cierre debe ser un Administrador.')

    def save(self, *args, **kwargs):
        # Si la caja está abierta, actualizamos los ingresos y egresos antes de guardar
        if self.estado == self.ABIERTO:
            # Consultar los movimientos relacionados con esta caja, filtrados por tipo "Ingreso" y "Egreso"
            movimientos_ingresos = Movimiento.objects.filter(id_caja=self, tipo=Movimiento.INGRESO)
            movimientos_egresos = Movimiento.objects.filter(id_caja=self, tipo=Movimiento.EGRESO)
            
            # Calcular la suma de los montos de ingresos y egresos
            self.ingresos = movimientos_ingresos.aggregate(total_ingresos=Sum('monto'))['total_ingresos'] or 0
            self.egresos = movimientos_egresos.aggregate(total_egresos=Sum('monto'))['total_egresos'] or 0

        # Si la fecha de apertura es anterior al día de hoy y la caja está abierta, cerramos la caja automáticamente
        now = timezone.now()
        if self.estado == self.ABIERTO and self.fecha_apertura.date() < now.date():
            self.fecha_cierre = now
            self.estado = self.CERRADO

        super(Caja, self).save(*args, **kwargs)

    def __str__(self):
        return f"Caja {self.id_caja} - Estado: {self.get_estado_display()}"

class Pago(models.Model):
    EFECTIVO = 'Efectivo'
    CREDITO = 'Crédito'
    DEBITO = 'Débito'
    TRANSFERENCIA = 'Transferencia'
    BILLETERA_VIRTUAL = 'Billetera Virtual'
    
    MEDIO_PAGO_CHOICES = [
        (EFECTIVO, 'Efectivo'),
        (CREDITO, 'Crédito'),
        (DEBITO, 'Débito'),
        (TRANSFERENCIA, 'Transferencia'),
        (BILLETERA_VIRTUAL, 'Billetera Virtual'),
    ]
    
    id_pagos = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    medio_pago = models.CharField(max_length=50, choices=MEDIO_PAGO_CHOICES)
    cuotas = models.ManyToManyField(Cuota, blank=True)
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"Pago {self.id_pagos} - {self.monto} - {self.medio_pago}"

class Movimiento(models.Model):
    INGRESO = 'Ingreso'
    EGRESO = 'Egreso'
    TIPO_CHOICES = [
        (INGRESO, 'Ingreso'),
        (EGRESO, 'Egreso'),
    ]
    
    id_movimientos = models.AutoField(primary_key=True)
    id_caja = models.ForeignKey(Caja, related_name='movimientos', on_delete=models.CASCADE)
    fecha_y_hora = models.DateTimeField()
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    id_pago = models.ForeignKey(Pago, related_name='movimientos', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Añadir ForeignKey a User
    usuario = models.ForeignKey(User, related_name='movimientos', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Movimiento {self.id_movimientos} - Tipo: {self.tipo} - Monto: {self.monto}"

