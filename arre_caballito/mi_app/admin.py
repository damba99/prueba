from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Alumnos)
admin.site.register(Competencia)
admin.site.register(Profesor)
admin.site.register(Categoria)
admin.site.register(Clase)
admin.site.register(Turno)
admin.site.register(Cuota)
admin.site.register(Caballo)
admin.site.register(Montura)
admin.site.register(Raza)
admin.site.register(Disciplina)
admin.site.register(AlumnosXCompetencia)
admin.site.register(AlumnosXClase)
admin.site.register(CaballoXRaza)
admin.site.register(CaballoXDisciplina)