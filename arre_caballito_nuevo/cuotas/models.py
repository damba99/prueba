from django.db import models
from alumnos.models import Alumno
from cajas.models import Pago

class Cuota(models.Model):
    MONTH_CHOICES = [
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    ]
        
    id_cuota = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='cuotas')
    mes = models.CharField(max_length=2, choices=MONTH_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField()
    
    def __str__(self):
        return f"Cuota {self.mes} - {self.alumno}"

class CuotasPorPago(models.Model):
    id_cuotas = models.ForeignKey(Cuota, related_name='cuotas_por_pago', on_delete=models.CASCADE)
    id_pago = models.ForeignKey(Pago, related_name='cuotas_por_pago', on_delete=models.CASCADE)

    def __str__(self):
        return f"Cuota {self.id_cuotas.id_cuotas} - Pago {self.id_pago.id_pagos}"
