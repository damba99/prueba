from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nuestra_historia/', views.nuestra_historia, name='nuestra_historia'),
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('login/', views.login, name='login'),
    path('administracion/', views.ubicacion, name='administracion'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('logout/', views.logout_view, name='logout'),
]