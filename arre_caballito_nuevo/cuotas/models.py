from django.db import models
from alumnos.models import Alumno, AlumnoClase
from clases.models import Disciplina
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date

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

class Monto(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='montos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    


class Cuota(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencida', 'Vencida'),
        ('proximo', 'Próximo'),
        ('cancelada', 'Cancelada'),
    ]
    
    id_cuota = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(AlumnoClase, on_delete=models.CASCADE, related_name='cuotas_alumno')
    id_periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='cuotas', blank=True, null=True)
    monto = models.ForeignKey(Monto, on_delete=models.CASCADE, related_name='cuotas')
    fecha_pago = models.DateField(null=True, blank=True)
    detalle = models.ForeignKey(AlumnoClase, on_delete=models.CASCADE, related_name='cuotas_detalle', blank=True, null=True)      
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Cuota {self.id_cuota} - {self.id_periodo} - {self.estado}"

    def clean(self):
        # Calcular fecha de vencimiento (asegurándose de que sea de tipo `date`)
        if self.id_periodo:
            anio = self.id_periodo.anio
            mes = self.id_periodo.mes
            mes = int(mes)
            # Convertir la fecha de vencimiento a un objeto `date` en vez de una cadena
            self.fecha_vencimiento = date(anio, mes, 10)
        
        # Establecer el estado en base a la fecha de vencimiento
        current_date = timezone.now().date()

        if self.estado != 'pagado':
            if current_date > self.fecha_vencimiento:
                self.estado = 'vencida'
            elif current_date < self.fecha_vencimiento and current_date.year == self.fecha_vencimiento.year and current_date.month == self.fecha_vencimiento.month:
                self.estado = 'pendiente'
            elif current_date.month < self.fecha_vencimiento.month or (current_date.month == self.fecha_vencimiento.month and current_date.day < self.fecha_vencimiento.day):
                self.estado = 'proximo'

    def save(self, *args, **kwargs):
        # Verificar si ya existe una cuota con los mismos datos
        if not Cuota.objects.filter(alumno=self.alumno, detalle=self.detalle, id_periodo=self.id_periodo).exists():
            # Si no existe, guardamos la cuota
            self.clean()  # Ejecutamos la validación personalizada antes de guardar
            super(Cuota, self).save(*args, **kwargs)
        # Si ya existe una cuota con los mismos datos, no se guarda nada
