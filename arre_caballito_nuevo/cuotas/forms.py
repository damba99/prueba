from django import forms
from .models import Cuota

class CuotaForm(forms.ModelForm):
    class Meta:
        model = Cuota
        fields = ['alumno', 'mes', 'monto', 'fecha_pago']
        widgets = {
            'fecha_pago': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }