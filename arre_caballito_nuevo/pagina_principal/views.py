from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CodigoRecuperacion
from django.utils import timezone
from alumnos.models import Alumno
from django.contrib.auth.hashers import make_password
import re
import random
from django.contrib.auth import update_session_auth_hash



def inicio(request):
    return render(request, 'inicio.html')

def nuestra_historia(request):
    return render(request, 'nuestra_historia.html')

def servicios(request):
    return render(request, 'servicios.html')

def contacto(request):
    return render(request, 'contacto.html')

def ubicacion(request):
    return render(request, 'ubicacion.html')

def login(request):
    return render(request, 'login.html')

def administracion(request):
    return render(request, 'administracion.html')

def iniciar_sesion(request):
    todos_los_usuarios = User.objects.all()
    print("Lista de todos los usuarios:")
    for u in todos_los_usuarios:
        print(f"- {u.username} | Email: {u.email} | Activo: {u.is_active}")

    if request.method == "POST":
        username = request.POST.get('username')
        password_o_codigo = request.POST.get('password')

        user = authenticate(request, username=username, password=password_o_codigo)
        print("hola")
        alumno = Alumno.objects.filter(usuario=user).first()
        if alumno:    
            print(alumno.dni)
        else:
            print("Nadita")

        no_dni = False
        
        if user is not None:
            auth_login(request, user)
            if alumno and alumno.dni == password_o_codigo:
                print("primer inicio de sesión")
                if no_dni == True:
                    return redirect('nueva_password')
            print(f"Acceso correcto con contraseña. Datos del usuario: {user}")
            return redirect('horarios')
        
        try:
            user = User.objects.get(username=username)
            codigo_obj = CodigoRecuperacion.objects.get(usuario=user)
            print(codigo_obj.activo)
            if codigo_obj.codigo == password_o_codigo and codigo_obj.activo == True:
                auth_login(request, user)
                print(f"Acceso correcto con código de recuperación. Datos del usuario: {user}")
                return redirect('nueva_password')
            else:
                print("Código de recuperación inválido o expirado.")
                return render(request, 'login.html', {'error': 'Contraseña o código incorrecto'})
        except (User.DoesNotExist, CodigoRecuperacion.DoesNotExist):
            print("Usuario no encontrado o no tiene un código de recuperación.")
            return render(request, 'login.html', {'error': 'Contraseña o código incorrecto'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def recuperar_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            codigo = CodigoRecuperacion.generar_codigo(user)
            obj, creado = CodigoRecuperacion.objects.update_or_create(
                usuario=user,
                defaults={'codigo': codigo, 'creado': timezone.now()}
            )
            print("Código de recuperación:", codigo)
        except User.DoesNotExist:
            print("Este correo no está registrado")
            return render(request, 'recuperar_password.html', {'error': 'Este correo no está registrado'})
        
        return redirect('login')

    return render(request, 'recuperar_password.html')

def nueva_password(request):
    if request.method == 'POST':
        nueva_pass = request.POST.get('nueva_pass')
        confirmar_pass = request.POST.get('confirmar_pass')

        if nueva_pass != confirmar_pass:
            return render(request, 'nueva_password.html', {'error': 'Las contraseñas no coinciden.'})

        if not re.search(r'[A-Z]', nueva_pass) or not re.search(r'\d', nueva_pass):
            return render(request, 'nueva_password.html', {
                'error': 'La contraseña debe contener al menos una letra mayúscula y un número.'
            })

        # Usuario autenticado (ya sea por código o login normal)
        user = request.user

        # Buscar código activo vinculado al usuario
        codigo_activo = CodigoRecuperacion.objects.filter(usuario=user, activo=True).first()
        if codigo_activo:
            print("Código activo encontrado")
            codigo_activo.activo = False

            if codigo_activo.usado == False:
                print("Código ya usado, desactivando")
                codigo_activo.activo = False
                codigo_activo.save()

            # Cambiar contraseña
            user.set_password(nueva_pass)
            user.save()
            update_session_auth_hash(request, user)

        return redirect('horarios')

    return render(request, 'nueva_password.html')

@login_required
def perfil(request):
    return redirect(f'/usuarios/id{request.user.id}/')
