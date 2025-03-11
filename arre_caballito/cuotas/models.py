from django.db import models

class Cuota(models.Model):
    id_cuota = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()

    def __str__(self):
        return f"Cuota {self.mes} - {self.alumno}"
