# forms.py

from django import forms
from .models import Categoria, Disciplina, Clase, Sesion

# Formulario para Categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

# Formulario para Disciplina
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nombre']

# Formulario para Clase
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['id_disciplina', 'id_categoria']

    # Si necesitaras campos como hora_inicio y hora_fin, agregarías algo como:
    # hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    # hora_fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

# Formulario para Sesion
class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = ['id_clase', 'id_profesor', 'dia', 'turno', 'hora_inicio', 'hora_fin']
    
    # El tipo de hora se puede ajustar a través de los widgets de Django
    hora_inicio = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    hora_fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
