from django import forms
from .models import Periodo, Monto, Cuota
from alumnos.models import AlumnoClase

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['anio', 'mes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anio'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['mes'].widget = forms.Select(attrs={'class': 'form-control'})


class MontoForm(forms.ModelForm):
    class Meta:
        model = Monto
        fields = ['disciplina', 'monto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['monto'].widget = forms.NumberInput(attrs={'class': 'form-control'})


class CuotaForm(forms.ModelForm):
    class Meta:
        model = Cuota
        fields = ['alumno', 'id_periodo', 'monto', 'fecha_pago', 'detalle', 'estado', 'fecha_vencimiento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alumno'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['id_periodo'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['monto'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['fecha_pago'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        self.fields['detalle'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['estado'].widget = forms.Select(attrs={'class': 'form-control'})
        self.fields['fecha_vencimiento'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
