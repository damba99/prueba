from django.db import models
from alumnos.models import Alumno

class Periodo(models.Model):
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
    anio = models.PositiveIntegerField()
    mes = models.CharField(max_length=2, choices=MONTH_CHOICES)

    def __str__(self):
        return f"{self.mes} - {self.anio}"

    class Meta:
        unique_together = ('anio', 'mes')


class Cuota(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencida', 'Vencida'),
    ]
    
    id_cuota = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='cuotas')
    id_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='cuotas', blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(null=True, blank=True)      
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Cuota {self.id_cuota} - {self.id_periodo} - {self.estado}"
