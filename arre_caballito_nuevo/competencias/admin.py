from django.contrib import admin
from .models import Competencia, Evento, Inscripcion

admin.site.register(Competencia)
admin.site.register(Evento)
admin.site.register(Inscripcion)