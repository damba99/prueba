
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pagina_principal.urls')), 
    path('alumnos', include('alumnos.urls')),
    path('profesores', include('profesores.urls')),
    path('clases', include('clases.urls')),
    path('caballos', include('caballos.urls')),
    path('cuotas', include('cuotas.urls')),
    path('cajas', include('cajas.urls')),
]
