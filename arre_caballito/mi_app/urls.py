from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nuestra_historia/', views.nuestra_historia, name='nuestra_historia'),
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('ubicacion/', views.ubicacion, name='ubicacion'),
    path('administracion/', views.administracion, name='administracion'),
    path('lista_alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('lista_profesor/', views.lista_profesor, name='lista_profesor'),
    path('lista_competencia/', views.lista_competencia, name='lista_competencia'),
    path('lista_categoria', views.lista_categoria, name='lista_categoria'),
    path('lista_clase/', views.lista_clase, name='lista_clase'),
    path('lista_turno/', views.lista_turno, name='lista_turno'),
    path('lista_cuota/', views.lista_cuota, name='lista_cuota'),
    path('lista_caballo/', views.lista_caballo, name='lista_caballo'),
    path('agregar_alumno/', views.agregar_alumno, name='agregar_alumno'),
    path('perfil_usuario/', views.perfil_alumno, name='perfil_usuario'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('eliminar_alumno/<int:id_alumno>/', views.eliminar_alumno, name='eliminar_alumno'),
    path('modificar_alumno/<int:id_alumno>/', views.modificar_alumno, name='modificar_alumno'),
    path('agregar_competencia/', views.agregar_competencia, name='agregar_competencia'),
    
    # Agregar estas nuevas rutas en urls.py
    path('eliminar_competencia/<int:id_competencia>/', views.eliminar_competencia, name='eliminar_competencia'),
    path('modificar_competencia/<int:id_competencia>/', views.modificar_competencia, name='modificar_competencia'),

    # Agregar estas nuevas rutas
    path('agregar_profesor/', views.agregar_profesor, name='agregar_profesor'),
    path('eliminar_profesor/<int:id_profesor>/', views.eliminar_profesor, name='eliminar_profesor'),
    path('modificar_profesor/<int:id_profesor>/', views.modificar_profesor, name='modificar_profesor'),

    path('agregar_categoria/', views.agregar_categoria, name='agregar_categoria'),
    path('modificar_categoria/<int:id_categoria>/', views.modificar_categoria, name='modificar_categoria'),
    path('eliminar_categoria/<int:id_categoria>/', views.eliminar_categoria, name='eliminar_categoria'),
    
    path('agregar_turno/', views.agregar_turno, name='agregar_turno'),
    path('modificar_turno/<int:id_turno>/', views.modificar_turno, name='modificar_turno'),
    path('eliminar_turno/<int:id_turno>/', views.eliminar_turno, name='eliminar_turno'),
    
    path('modificar_caballo/<int:id_caballo>/', views.modificar_caballo, name='modificar_caballo'),
    path('eliminar_caballo/<int:id_caballo>/', views.eliminar_caballo, name='eliminar_caballo'),
    path('agregar_caballo/', views.agregar_caballo, name='agregar_caballo'),
    path('lista_caballos/', views.lista_caballos, name='lista_caballos'),
    
    ## cuotas
    path('lista_cuota/', views.lista_cuota, name='lista_cuota'),
    path('agregar_cuota/', views.agregar_cuota, name='agregar_cuota'),
    path('modificar_cuota/<int:id_cuota>/', views.modificar_cuota, name='modificar_cuota'),
    path('eliminar_cuota/<int:id>/', views.eliminar_cuota, name='eliminar_cuota'),

    ## razas
    path('lista_raza/', views.lista_raza, name='lista_raza'),
    path('agregar_raza/', views.agregar_raza, name='agregar_raza'),
    path('modificar_raza/<int:id_raza>/', views.modificar_raza, name='modificar_raza'),
    path('eliminar_raza/<int:id_raza>/', views.eliminar_raza, name='eliminar_raza'),
    
    ## moonturas
    path('lista_montura/', views.lista_montura, name='lista_montura'),
    path('agregar_montura/', views.agregar_montura, name='agregar_montura'),
    path('modificar_montura/<int:id_montura>/', views.modificar_montura, name='modificar_montura'),
    path('eliminar_montura/<int:id_montura>/', views.eliminar_montura, name='eliminar_cuota'),
    
    ## clase
    path('lista_clase/', views.lista_clase, name='lista_clase'),
    path('agregar_clase/', views.agregar_clase, name='agregar_clase'),
    path('modificar_clase/<int:id_clase>/', views.modificar_clase, name='modificar_clase'),
    path('eliminar_clase/<int:id_clase>/', views.eliminar_clase, name='eliminar_clase'),
    
    ## discliplinas
    path('lista_disciplina/', views.lista_disciplina, name='lista_disciplina'),
    path('agregar_disciplina/', views.agregar_disciplina, name='agregar_disciplina'),
    path('modificar_disciplina/<int:id_disciplina>/', views.modificar_disciplina, name='modificar_disciplina'),
    path('eliminar_disciplina/<int:id_disciplina>/', views.eliminar_disciplina, name='eliminar_disciplina'),
    
    ## alumno x competencia
    path('lista_alumnoxcompetencia/', views.lista_alumnoxcompetencia, name='lista_alumnoxcompetencia'),
    path('agregar_alumnoxcompetencia/', views.agregar_alumnoxcompetencia, name='agregar_alumnoxcompetencia'),
    path('modificar_alumnoxcompetencia/<int:id_alumnos_competencia>/', views.modificar_alumnoxcompetencia,name='modificar_alumnoxcompetencia'),
    path('eliminar_alumnoxcompetencia/<int:id_alumnos_competencia>/', views.eliminar_alumnoxcompetencia,name='eliminar_alumnoxcompetencia'),

    ## alumno por clase
    path('lista_alumnoxclase/', views.lista_alumnoxclase, name='lista_alumnoxclase'),
    path('agregar_alumnoxclase/', views.agregar_alumnoxclase, name='agregar_alumnoxclase'),
    path('modificar_alumnoxclase/<int:id_alumnos_clase>/', views.modificar_alumnoxclase, name='modificar_alumnoxclase'),
    path('eliminar_alumnoxclase/<int:id_alumnos_clase>/', views.eliminar_alumnoxclase,name='eliminar_alumnoxclase'),
    
    

    ]