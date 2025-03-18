from django import forms
from .models import Categoria, Disciplina, Clase, Sesion
from profesores.models import Profesor

# Formulario para Categoria
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la categoría',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para Disciplina
class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la disciplina',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para Clase
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['nombre', 'id_disciplina', 'id_categoria']
        labels = {
            'nombre': 'Nombre de la clase',
            'id_disciplina': 'Disciplina',
            'id_categoria': 'Categoría',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'id_disciplina': forms.Select(attrs={'class': 'form-control'}),
            'id_categoria': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para Sesion
class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = ['id_profesor', 'dia', 'id_clase', 'hora_inicio', 'hora_fin']
        labels = {
            'id_profesor': 'Profesor',
            'dia': 'Día de la sesión',
            'id_clase': 'Clase asociada',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
        }
        widgets = {
            'id_profesor': forms.Select(attrs={'class': 'form-control'}),
            'dia': forms.Select(choices=Sesion.DIA_CHOICES, attrs={'class': 'form-control'}),
            'id_clase': forms.Select(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
