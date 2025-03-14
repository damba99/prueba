from django import forms
from .models import Disciplina, Caballo

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nombre']

class CaballoForm(forms.ModelForm):
    class Meta:
        model = Caballo
        fields = ['nombre', 'edad', 'sexo', 'disciplinas']