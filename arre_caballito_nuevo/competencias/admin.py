from django.contrib import admin
from .models import Competencia, Evento, Inscripcion_competencia

admin.site.register(Competencia)
admin.site.register(Evento)
admin.site.register(Inscripcion_competencia)