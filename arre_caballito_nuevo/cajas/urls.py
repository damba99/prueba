from django.urls import path
from . import views

urlpatterns = [
    path('', views.apertura_caja, name='apertura_caja'),
    path('detalle_caja/<int:pk>/', views.detalle_caja, name='detalle_caja'),
    path('cerrar_caja/<int:pk>/', views.cerrar_caja, name='cerrar_caja'),
    path('listar_cajas/', views.listar_cajas, name='listar_cajas'),
    path('registrar_movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
    path('movimientos/<int:pk>/', views.movimientos_caja, name='movimientos_caja'),

]
