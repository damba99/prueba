from django.contrib import admin
from .models import Cuota, Monto, Periodo, Inscripcion

admin.site.register(Cuota)
admin.site.register(Monto)
admin.site.register(Periodo)
admin.site.register(Inscripcion)
