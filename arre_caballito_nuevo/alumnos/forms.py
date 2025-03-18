from django import forms
from .models import Alumno, AlumnoClase, Asistencia
from caballos.models import Caballo
from clases.models import Sesion, Clase
from django.core.exceptions import ValidationError

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'direccion', 'telefono', 'email', 'id_categoria']

    def clean_dni(self):
        # Verifica que el DNI sea único
        dni = self.cleaned_data['dni']
        if Alumno.objects.filter(dni=dni).exists():
            raise ValidationError("Ya existe un alumno con este DNI.")
        return dni

class AlumnoClaseForm(forms.ModelForm):
    class Meta:
        model = AlumnoClase
        fields = ['alumno', 'clase']

    def clean(self):
        cleaned_data = super().clean()

        alumno = cleaned_data.get('alumno')
        clase = cleaned_data.get('clase')

        # Asegurarse de que el alumno no se inscriba dos veces en la misma clase
        if AlumnoClase.objects.filter(alumno=alumno, clase=clase).exists():
            raise ValidationError(f"El alumno {alumno} ya está inscrito en la clase {clase}.")

        return cleaned_data

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['id_sesion', 'id_alumno', 'id_caballo', 'fecha']

    def clean(self):
        cleaned_data = super().clean()

        id_sesion = cleaned_data.get('id_sesion')
        id_alumno = cleaned_data.get('id_alumno')

        # Validar si el alumno está inscrito en la clase correspondiente a la sesión
        if id_sesion and id_alumno:
            clase = id_sesion.id_clase  # Obtener la clase asociada a la sesión

            # Verificar si el alumno está inscrito en esa clase
            if not AlumnoClase.objects.filter(alumno=id_alumno, clase=clase).exists():
                raise ValidationError(f"El alumno {id_alumno} no está inscrito en la clase {clase}.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(AsistenciaForm, self).__init__(*args, **kwargs)

        # Personalización de los campos si es necesario
        self.fields['id_sesion'].queryset = Sesion.objects.all()
        self.fields['id_alumno'].queryset = Alumno.objects.all()
        self.fields['id_caballo'].queryset = Caballo.objects.all()
        self.fields['fecha'].widget.attrs['type'] = 'date'  # Establecer