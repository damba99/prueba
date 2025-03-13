from django.contrib import admin
from .models import Caballo, CaballosPorDisciplina, Disciplina

admin.site.register(Caballo)
admin.site.register(CaballosPorDisciplina)
admin.site.register(Disciplina)