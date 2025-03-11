from django import forms
from .models import *

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = '__all__'

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = '__all__'

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'

class CuotaForm(forms.ModelForm):
    class Meta:
        model = Cuota
        fields = ['alumno', 'mes', 'monto', 'fecha_pago',]  # Asegúrate de incluir todos los campos necesarios
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }

class CaballoForm(forms.ModelForm):
    class Meta:
        model = Caballo
        fields = '__all__'

class MonturaForm(forms.ModelForm):
    class Meta:
        model = Montura
        fields = '__all__'

class RazaForm(forms.ModelForm):
    class Meta:
        model = Raza
        fields = ('nombre',)


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'

class AlumnosXCompetenciaForm(forms.ModelForm):
    class Meta:
        model = AlumnosXCompetencia
        fields = '__all__'

class AlumnosXClaseForm(forms.ModelForm):
    class Meta:
        model = AlumnosXClase
        fields = '__all__'

class CaballoXRazaForm(forms.ModelForm):
    class Meta:
        model = CaballoXRaza
        fields = '__all__'

class CaballoXDisciplinaForm(forms.ModelForm):
    class Meta:
        model = CaballoXDisciplina
        fields = '__all__'
        
class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono', 'email']

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono', 'email']

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = ['nombre', 'direccion', 'fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),}

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        
class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['categoria', 'hora_inicio', 'hora_fin']
        
class CaballoForm(forms.ModelForm):
    class Meta:
        model = Caballo
        fields = ['nombre', 'edad', 'sexo']

