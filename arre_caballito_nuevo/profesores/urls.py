from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_profesores, name='listar_profesores'),
    path('crear/', views.crear_profesor, name='crear_profesor'),
    path('<int:pk>/', views.detalle_profesor, name='detalle_profesor'),
    path('<int:pk>/modificar/', views.modificar_profesor, name='modificar_profesor'),
    path('<int:pk>/eliminar/', views.eliminar_profesor, name='eliminar_profesor'),
]
