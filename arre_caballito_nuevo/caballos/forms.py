from django import forms
from .models import Caballo

class CaballoForm(forms.ModelForm):
    class Meta:
        model = Caballo
        fields = ['nombre', 'edad', 'sexo', 'disciplinas']