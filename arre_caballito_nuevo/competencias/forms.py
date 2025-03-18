from django import forms
from .models import Competencia, Evento, Inscripcion_competencia

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

class Inscripcion_competenciaForm(forms.ModelForm):
    class Meta:
        model = Inscripcion_competencia
        fields = ['id_competencia', 'id_alumno', 'id_caballo', 'id_evento']