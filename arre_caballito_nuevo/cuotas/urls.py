from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_cuotas, name='listar_cuotas'),
]