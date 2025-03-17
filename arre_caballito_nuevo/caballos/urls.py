from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_caballos, name='listar_caballos'),
    path('crear/', views.crear_caballo, name='crear_caballo'),
    path('<int:pk>/', views.detalle_caballo, name='detalle_caballo'),
    path('<int:pk>/modificar/', views.modificar_caballo, name='modificar_caballo'),
    path('<int:pk>/eliminar/', views.eliminar_caballo, name='eliminar_caballo'),
]
