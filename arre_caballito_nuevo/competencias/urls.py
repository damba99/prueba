# competencias/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_competencias, name='listar_competencias'),
    path('crear/', views.crear_competencia, name='crear_competencia'),
    path('detalles_competencia/<int:id_competencia>/', views.detalles_competencia, name='detalles_competencia'),
    path('agregar_evento/<int:id_competencia>/', views.agregar_evento, name='agregar_evento'),
]