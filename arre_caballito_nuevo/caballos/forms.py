# forms.py
from django import forms
from .models import Caballo, CaballoDisciplina
from clases.models import Disciplina

class CaballoForm(forms.ModelForm):
    class Meta:
        model = Caballo
        fields = ['nombre', 'edad', 'sexo']

class CaballoDisciplinaForm(forms.ModelForm):
    class Meta:
        model = CaballoDisciplina
        fields = ['caballo', 'disciplina']
