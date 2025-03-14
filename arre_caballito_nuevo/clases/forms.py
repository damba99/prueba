from django import forms
from .models import Categoria, Clase, Asistencia

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['fecha', 'hora_inicio', 'hora_fin', 'id_profesor', 'id_disciplina', 'id_categoria']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['id_clase', 'id_alumno', 'id_caballo']