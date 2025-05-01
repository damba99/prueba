from django.urls import path
from . import views

urlpatterns = [
    path('apertura_caja/', views.apertura_caja, name='apertura_caja'),
    path('detalle_caja/<int:pk>/', views.detalle_caja, name='detalle_caja'),
    path('cerrar_caja/<int:pk>/', views.cerrar_caja, name='cerrar_caja'),
    path('', views.listar_cajas, name='listar_cajas'),
    path('registrar_movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
    path('movimientos/<int:pk>/', views.movimientos_caja, name='movimientos_caja'),

]
