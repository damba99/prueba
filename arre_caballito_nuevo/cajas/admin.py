from django.contrib import admin
from .models import Caja, Pago, Movimiento

admin.site.register(Caja)
admin.site.register(Pago)
admin.site.register(Movimiento)
