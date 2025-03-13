from django.contrib import admin
from .models import Categoria, Disciplina, Clase, Asistencia

admin.site.register(Categoria)
admin.site.register(Disciplina)
admin.site.register(Clase)
admin.site.register(Asistencia)
