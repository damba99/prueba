from django import forms
from .models import Competencia, Evento, Inscripcion

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = ['nombre', 'descripcion', 'lugar', 'fecha_hora']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['id_competencia', 'id_disciplina', 'id_categoria']

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['id_competencia', 'id_alumno', 'id_caballo', 'id_evento']