from django import forms
from .models import Caja, Pago, Movimiento

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['usuario_apertura', 'usuario_cierre', 'fecha_apertura', 'fecha_cierre', 'monto_inicial', 'monto_final', 'ingresos', 'egresos', 'saldo', 'estado']
        widgets = {
            'fecha_apertura': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_cierre': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha_hora', 'monto', 'medio_pago', 'cuotas']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['id_caja', 'fecha_y_hora', 'tipo', 'monto', 'descripcion', 'id_pago']
        widgets = {
            'fecha_y_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }