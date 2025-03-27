from django.urls import path
from . import views

urlpatterns = [
    path('cuotas/', views.listar_cuotas, name='listar_cuotas'),
    path('listar_montos/', views.listar_montos, name='listar_montos'),
    path('<int:pk>/modificar_monto/', views.modificar_monto, name='modificar_monto'),
    path('<int:pk>/modificar_cuota/', views.modificar_cuota, name='modificar_cuota'),
    path('', views.cuotas, name='cuotas'),
    path('<int:pk>/deudas/', views.deudas, name='deudas'),
    path('registrar_pago/<int:pk>/', views.registrar_pago, name='registrar_pago'),
    path('pagar/<int:pk>/', views.pagar, name='pagar'),



]