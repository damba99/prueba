from django import forms
from .models import Alumno, AlumnoSesion, Asistencia
from caballos.models import Caballo
from clases.models import Sesion

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono', 'email', 'id_categoria']

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if len(dni) <= 7:
            raise forms.ValidationError("El DNI debe tener más de 7 caracteres.")
        return dni

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Alumno.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un alumno con este correo electrónico.")
        return email

class AlumnoSesionForm(forms.ModelForm):
    class Meta:
        model = AlumnoSesion
        fields = ['alumno', 'sesion']

    def clean(self):
        cleaned_data = super().clean()
        alumno = cleaned_data.get("alumno")
        sesion = cleaned_data.get("sesion")

        if AlumnoSesion.objects.filter(alumno=alumno, sesion=sesion).exists():
            raise forms.ValidationError("El alumno ya está inscrito en esta sesión.")

        return cleaned_data

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['id_sesion', 'id_alumno', 'id_caballo', 'fecha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'id_sesion' in self.data:
            try:
                sesion_id = self.data.get('id_sesion')
                sesion = Sesion.objects.get(id=sesion_id)
                self.fields['id_caballo'].queryset = Caballo.objects.filter(disciplinas=sesion.id_clase.id_disciplina)
            except (Sesion.DoesNotExist, ValueError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        id_alumno = cleaned_data.get('id_alumno')
        id_sesion = cleaned_data.get('id_sesion')
        id_caballo = cleaned_data.get('id_caballo')

        # Validación para verificar si el alumno está inscrito en la sesión
        if not AlumnoSesion.objects.filter(alumno=id_alumno, sesion=id_sesion).exists():
            raise forms.ValidationError(f"El alumno no está inscrito en la sesión {id_sesion.id_clase.nombre}.")

        # Validación para verificar si el caballo está asociado con la disciplina de la clase
        if id_caballo:
            clase_sesion = id_sesion.id_clase
            if id_caballo.disciplinas.filter(id=clase_sesion.id_disciplina.id).exists() is False:
                raise forms.ValidationError(f"El caballo {id_caballo.nombre} no está asociado a la disciplina {clase_sesion.id_disciplina.nombre}.")

        return cleaned_data
