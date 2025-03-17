from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_alumnos, name='listar_alumnos'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('<int:pk>/', views.detalle_alumno, name='detalle_alumno'),
    path('<int:pk>/modificar/', views.modificar_alumno, name='modificar_alumno'),
    path('<int:pk>/eliminar/', views.eliminar_alumno, name='eliminar_alumno'),
]
