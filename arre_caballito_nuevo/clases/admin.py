from django.contrib import admin
from .models import Categoria, Sesion, Clase, Disciplina

admin.site.register(Categoria)
admin.site.register(Clase)
admin.site.register(Disciplina)
admin.site.register(Sesion)
