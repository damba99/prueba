from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CodigoRecuperacion
from django.utils import timezone
import random


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

        # Intentamos autenticar con nombre de usuario y contraseña
        user = authenticate(request, username=username, password=password_o_codigo)

        if user is not None:
            # Si la autenticación con la contraseña es exitosa
            auth_login(request, user)
            print(f"Acceso correcto con contraseña. Datos del usuario: {user}")
            return redirect('horarios')
        try:
            user = User.objects.get(username=username)
            codigo_obj = CodigoRecuperacion.objects.get(usuario=user)

            if codigo_obj.codigo == password_o_codigo and codigo_obj.es_valido():
                # Si el código de recuperación es válido
                auth_login(request, user)
                print(f"Acceso correcto con código de recuperación. Datos del usuario: {user}")
                return redirect('horarios')
            else:
                print("Código de recuperación inválido o expirado.")
                return HttpResponse("Código de recuperación inválido o expirado.")
        except (User.DoesNotExist, CodigoRecuperacion.DoesNotExist):
            # Si no se encuentra el usuario o no tiene código de recuperación
            print("Usuario no encontrado o no tiene un código de recuperación.")
            return HttpResponse("Usuario no encontrado o no tiene un código de recuperación.")

    return render(request, 'inicio.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def recuperar_apassword(request):
    error = ""
    email_valido = True
    codigo_generado = None

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            codigo_generado = str(random.randint(100000, 999999))
            print(f"Contraseña recuperada. Código generado: {codigo_generado}")
        except User.DoesNotExist:
            error = "Este correo no está registrado"
            email_valido = False

    return render(request, "recuperar_password.html", {
        "error": error,
        "email_valido": email_valido,
    })

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
    return render(request, 'recuperar_password.html')

@login_required
def perfil(request):
    return redirect(f'/usuarios/id{request.user.id}/')
