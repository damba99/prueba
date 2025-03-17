from django.urls import path
from . import views

urlpatterns = [
    # Sesiones
    path('', views.listar_sesiones, name='listar_sesiones'),
    path('sesion/crear/', views.crear_sesion, name='crear_sesion'),
    path('sesion/<int:pk>/', views.detalle_sesion, name='detalle_sesion'),
    path('sesion/<int:pk>/modificar/', views.modificar_sesion, name='modificar_sesion'),
    path('sesion/<int:pk>/eliminar/', views.eliminar_sesion, name='eliminar_sesion'),

    # Clases
    path('clase/', views.listar_clases, name='listar_clases'),
    path('clase/crear/', views.crear_clase, name='crear_clase'),
    path('clase/<int:pk>/modificar/', views.modificar_clase, name='modificar_clase'),
    path('clase/<int:pk>/eliminar/', views.eliminar_clase, name='eliminar_clase'),
    path('clase/<int:pk>/', views.detalle_clase, name='detalle_clase'),
]
