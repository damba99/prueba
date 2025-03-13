from django.db import models
from usuarios.models import Usuario
from django.core.exceptions import ValidationError
from cuotas.models import Cuota

class Caja(models.Model):
    ABIERTO = 'Abierta'
    CERRADO = 'Cerrada'
    ESTADO_CHOICES = [
        (ABIERTO, 'Abierta'),
        (CERRADO, 'Cerrada'),
    ]
    
    id_caja = models.AutoField(primary_key=True)
    usuario_apertura = models.ForeignKey(Usuario, related_name='usuario_apertura', on_delete=models.CASCADE)
    usuario_cierre = models.ForeignKey(Usuario, related_name='usuario_cierre', on_delete=models.CASCADE)
    fecha_apertura = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2)
    ingresos = models.DecimalField(max_digits=10, decimal_places=2)
    egresos = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default=CERRADO)
    
    def clean(self):
        # Validar que ambos usuarios (apertura y cierre) sean Administradores
        if self.usuario_apertura.rol != 'Administrador':
            raise ValidationError('El usuario de apertura debe ser un Administrador.')
        if self.usuario_cierre.rol != 'Administrador':
            raise ValidationError('El usuario de cierre debe ser un Administrador.')
    
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
    fecha_hora = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    medio_pago = models.CharField(max_length=50, choices=MEDIO_PAGO_CHOICES)
    cuotas = models.ManyToManyField(Cuota)

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
    descripcion = models.TextField()
    id_pago = models.ForeignKey(Pago, related_name='movimientos', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Movimiento {self.id_movimientos} - Tipo: {self.tipo} - Monto: {self.monto}"


