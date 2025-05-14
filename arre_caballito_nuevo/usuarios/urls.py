from django.urls import path
from . import views

urlpatterns = [
    path('id<int:id>/', views.perfil, name='perfil'),
    path('foto/actualizar/', views.actualizar_foto_perfil, name='actualizar_foto_perfil'),
    path('foto/actualizar/<int:id>/', views.actualizar_foto_perfil, name='actualizar_foto_perfil_admin'),

]