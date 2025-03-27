from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse
from django.contrib.auth import login as auth_login  # Si usas el nuevo login del sistema de sesiones


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
    if request.method == "POST":
        # Obtener el nombre de usuario y la contraseña desde el formulario
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Intentar autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si la autenticación es exitosa, iniciar sesión usando el nuevo sistema
            auth_login(request, user)  # Esto es el "nuevo" login
            # Imprimir los detalles del usuario en la consola
            print(f"Acceso correcto. Datos del usuario: {user}")

            return redirect('horarios')
        else:
            # Si la autenticación falla, identificar el error
            print("Acceso incorrecto. Usuario o contraseña incorrectos.")
            return HttpResponse("Acceso incorrecto. Usuario o contraseña incorrectos.")
    
    # Si no es un POST, renderiza el formulario de inicio de sesión
    return render(request, 'inicio.html')

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')
