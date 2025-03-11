from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from .forms import AlumnoForm
from .forms import CuotaForm 
from .models import Alumnos
from .models import Cuota 
from django.contrib.admin.views.decorators import staff_member_required 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

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
def administracion(request):
    return render(request, 'administracion.html')

  # Solo accesible por el administrador (staff)
def lista_alumnos(request):
    alumnos = Alumnos.objects.all()  # Consulta: Obtener todos los registros de alumnos
    return render(request, 'lista_alumnos.html', {'alumnos': alumnos})

def lista_profesor(request):
    profesores = Profesor.objects.all()
    return render(request, 'lista_profesores.html', {'profesores': profesores})
def lista_competencia(request):
    competencias = Competencia.objects.all()
    return render(request, 'lista_competencias.html', {'competencias': competencias})
def lista_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})
def lista_clase(request):
    clases = Clase.objects.all()
    return render(request, 'lista_clases.html', {'clases': clases})
def lista_turno(request):
    turnos = Turno.objects.all()
    return render(request, 'lista_turnos.html', {'turnos': turnos})
def lista_cuota(request):
    cuotas = Cuota.objects.all()
    return render(request, 'lista_cuotas.html', {'cuotas': cuotas})
def lista_caballo(request):
    caballos = Caballo.objects.all()
    return render(request, 'lista_caballos.html', {'caballos': caballos})


## alumno
@login_required  # Para asegurar que solo usuarios logueados accedan
def perfil_alumno(request):
    # Obtener el usuario autenticado (el alumno) y su registro
    alumno = Alumnos.objects.filter(email=request.user.email).first()

    if request.method == 'POST':
        if alumno:  # Si ya existe, actualizar sus datos
            form = AlumnoForm(request.POST, instance=alumno)
        else:  # Si no existe, crear un nuevo registro
            form = AlumnoForm(request.POST)

        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.email = request.user.email  # Asegurar que el email del alumno coincida con su usuario logueado
            alumno.save()
            return render(request, 'perfil_usuario.html', {'alumno': alumno, 'form': form, 'mensaje': "Datos actualizados correctamente."})
    else:
        # Si el método es GET
        form = AlumnoForm(instance=alumno)  # Cargar datos existentes (si los hay) en el formulario

    return render(request, 'perfil_usuario.html', {'form': form, 'alumno': alumno})

def agregar_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()

    return render(request, 'agregar_alumno.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Profesores').exists():
            return redirect('lista_alumnos')
        elif request.user.groups.filter(name='Alumnos').exists():
            return redirect('perfil_usuario')
        else:
            return redirect('login')
    else:
        return redirect('login')

def eliminar_alumno(request, id_alumno):
    alumno = get_object_or_404(Alumnos, id_alumno=id_alumno)
    if request.method == 'POST':
        alumno.delete()
        return redirect('lista_alumnos')
    return redirect('lista_alumnos')

def modificar_alumno(request, id_alumno):
    alumno = get_object_or_404(Alumnos, id_alumno=id_alumno)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm(instance=alumno)
    
    return render(request, 'modificar_alumno.html', {'form': form, 'alumno': alumno})


## competencia

def agregar_competencia(request):
    if request.method == 'POST':
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('lista_competencia')
    else:
        form = CompetenciaForm()
    return render(request, 'agregar_competencia.html', {'form': form})



def eliminar_competencia(request, id_competencia):
    competencia = get_object_or_404(Competencia, id_competencia=id_competencia)
    if request.method == 'POST':
        competencia.delete()
        return redirect('lista_competencia')
    return redirect('lista_competencia')

def modificar_competencia(request, id_competencia):
    competencia = get_object_or_404(Competencia, id_competencia=id_competencia)
    if request.method == 'POST':
        form = CompetenciaForm(request.POST, instance=competencia)
        if form.is_valid():
            form.save()
            return redirect('lista_competencia')
    else:
        form = CompetenciaForm(instance=competencia)
    return render(request, 'modificar_competencia.html', {'form': form, 'competencia': competencia})

def agregar_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_profesor')
    else:
        form = ProfesorForm()
    return render(request, 'agregar_profesor.html', {'form': form})

def eliminar_profesor(request, id_profesor):
    profesor = get_object_or_404(Profesor, id_profesor=id_profesor)
    if request.method == 'POST':
        profesor.delete()
        return redirect('lista_profesor')
    return redirect('lista_profesor')

def modificar_profesor(request, id_profesor):
    profesor = get_object_or_404(Profesor, id_profesor=id_profesor)
    if request.method == 'POST':
        form = ProfesorForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('lista_profesor')
    else:
        form = ProfesorForm(instance=profesor)
    return render(request, 'modificar_profesor.html', {'form': form, 'profesor': profesor})


def lista_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'lista_categorias.html', {'categorias': categorias})

def agregar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categoria')
    else:
        form = CategoriaForm()
    return render(request, 'agregar_categoria.html', {'form': form})

def modificar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categoria')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'modificar_categoria.html', {'form': form, 'categoria': categoria})

def eliminar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categoria')
    return redirect('lista_categoria')

#turnos
# Vista para listar turnos
def lista_turno(request):
    turnos = Turno.objects.all()
    return render(request, 'lista_turnos.html', {'turnos': turnos})

# Vista para agregar un turno
def agregar_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_turno')
    else:
        form = TurnoForm()
    return render(request, 'agregar_turno.html', {'form': form})

# Vista para modificar un turno
def modificar_turno(request, id_turno):
    turno = get_object_or_404(Turno, id_turno=id_turno)
    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('lista_turno')
    else:
        form = TurnoForm(instance=turno)
    return render(request, 'modificar_turno.html', {'form': form, 'turno': turno})

# Vista para eliminar un turno
def eliminar_turno(request, id_turno):
    turno = get_object_or_404(Turno, id_turno=id_turno)
    if request.method == 'POST':
        turno.delete()
        return redirect('lista_turno')
    return render(request, 'confirmar_eliminar_turno.html', {'turno': turno})

## caballos

def lista_caballos(request):
    caballos = Caballo.objects.all()
    return render(request, 'lista_caballos.html', {'caballos': caballos})

def agregar_caballo(request):
    if request.method == 'POST':
        form = CaballoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_caballo')
    else:
        form = CaballoForm()
    return render(request, 'agregar_caballo.html', {'form': form})

def modificar_caballo(request, id_caballo):
    # Cambiar a 'id_caballo' en vez de 'id'
    caballo = get_object_or_404(Caballo, id_caballo=id_caballo)

    if request.method == 'POST':
        form = CaballoForm(request.POST, instance=caballo)
        if form.is_valid():
            form.save()
            return redirect('lista_caballos')  # Redirige a la lista de caballos
    else:
        form = CaballoForm(instance=caballo)

    return render(request, 'modificar_caballo.html', {'form': form})

def eliminar_caballo(request, id_caballo):
    # Usa 'id_caballo' en lugar de 'id' para buscar el objeto
    caballo = get_object_or_404(Caballo, id_caballo=id_caballo)

    if request.method == 'POST':
        caballo.delete()
        return redirect('lista_caballos')  # Redirige a la lista de caballos después de eliminar

    return render(request, 'confirmar_eliminacion.html', {'caballo': caballo})

## cuotas
# views.py

def agregar_cuota(request):
    if request.method == 'POST':
        form = CuotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cuota')
    else:
        form = CuotaForm()
    return render(request, 'agregar_cuota.html', {'form': form})

def modificar_cuota(request, id_cuota):
    cuota = get_object_or_404(Cuota, id_cuota=id_cuota)
    if request.method == 'POST':
        form = CuotaForm(request.POST, instance=cuota)
        if form.is_valid():
            form.save()
            return redirect('lista_cuota')
    else:
        form = CuotaForm(instance=cuota)
    return render(request, 'modificar_cuota.html', {'form': form, 'cuota': cuota})

def eliminar_cuota(request, id):  # Asegúrate de usar 'id' aquí
    if request.method == 'POST':
        cuota = get_object_or_404(Cuota, id_cuota=id)  # Usando 'id' como argumento
        cuota.delete()
        return redirect('lista_cuota')  # Cambiado de lista_cuotas a lista_cuota
    return redirect('lista_cuota')  # Cambiado de lista_cuotas a lista_cuota

def lista_cuota(request):
    cuotas = Cuota.objects.all()
    return render(request, 'lista_cuotas.html', {'cuotas': cuotas})

## razas
def lista_raza(request):
    razas = Raza.objects.all()
    return render(request, 'lista_razas.html', {'razas': razas})

def agregar_raza(request):
    if request.method == 'POST':
        form = RazaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_raza')
    else:
        form = RazaForm()
    return render(request, 'agregar_raza.html', {'form': form})

def modificar_raza(request, id_raza):
    raza = get_object_or_404(Raza, id_raza=id_raza)
    if request.method == 'POST':
        form = RazaForm(request.POST, instance=raza)
        if form.is_valid():
            form.save()
            return redirect('lista_raza')
    else:
        form = RazaForm(instance=raza)
    return render(request, 'modificar_raza.html', {'form': form, 'raza': raza})

def eliminar_raza(request, id_raza):
    raza = get_object_or_404(Raza, id_raza=id_raza)
    if request.method == 'POST':
        raza.delete()
        return redirect('lista_raza')
    return redirect('lista_raza')

## monturas

def agregar_montura(request):
    if request.method == 'POST':
        form = MonturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_montura')
    else:
        form = MonturaForm()
    return render(request, 'agregar_montura.html', {'form': form})

def modificar_montura(request, id_montura):
    montura = get_object_or_404(Montura, id_montura=id_montura)
    if request.method == 'POST':
        form = MonturaForm(request.POST, instance=montura)
        if form.is_valid():
            form.save()
            return redirect('lista_montura')
    else:
        form = MonturaForm(instance=montura)
    return render(request, 'modificar_montura.html', {'form': form, 'montura': montura})

def eliminar_montura(request, id):  # Asegúrate de usar 'id' aquí
    if request.method == 'POST':
        montura = get_object_or_404(Montura, id_montura=id)  # Usando 'id' como argumento
        montura.delete()
        return redirect('lista_montura')  # Cambiado de lista_cuotas a lista_cuota
    return redirect('lista_montura')  # Cambiado de lista_cuotas a lista_cuota

def lista_montura(request):
    monturas = Montura.objects.all()
    return render(request, 'lista_monturas.html', {'monturas': monturas})

## clase
def agregar_clase(request):
    if request.method == 'POST':
        form = ClaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clase')
    else:
        form = ClaseForm()
    return render(request, 'agregar_clase.html', {'form': form})

def modificar_clase(request, id_clase):
    clase = get_object_or_404(Clase, id_clase=id_clase)
    if request.method == 'POST':
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            form.save()
            return redirect('lista_clase')
    else:
        form = ClaseForm(instance=clase)
    return render(request, 'modificar_clase.html', {'form': form, 'clase': clase})

def eliminar_clase(request, id):
    if request.method == 'POST':
        clase = get_object_or_404(Clase, id_clase=id)
        clase.delete()
        return redirect('lista_clase')
    return redirect('lista_clase')

def lista_clase(request):
    clases = Clase.objects.all()
    return render(request, 'lista_clases.html', {'clases': clases})

## disciplinas
def lista_disciplina(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'lista_disciplinas.html', {'disciplinas': disciplinas})

def agregar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_disciplina')
    else:
        form = DisciplinaForm()
    return render(request, 'agregar_disciplina.html', {'form': form})

def modificar_disciplina(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, id_disciplina=id_disciplina)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('lista_disciplina')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'modificar_disciplina.html', {'form': form, 'disciplina': disciplina})

def eliminar_disciplina(request, id_disciplina):
    disciplina = get_object_or_404(Disciplina, id_disciplina=id_disciplina)
    if request.method == 'POST':
        disciplina.delete()
        return redirect('lista_disciplina')
    return redirect('lista_disciplina')

## alumnoxcompetencia 
def agregar_alumnoxcompetencia(request):
    if request.method == 'POST':
        form = AlumnosXCompetenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnoxcompetencia')
    else:
        form = AlumnosXCompetenciaForm()
    return render(request, 'agregar_alumnoxcompetencia.html', {'form': form})

def modificar_alumnoxcompetencia(request, id_alumnos_competencia):
    alumnoxcompetencia = get_object_or_404(AlumnosXCompetencia, id_alumnos_competencia=id_alumnos_competencia)
    if request.method == 'POST':
        form = AlumnosXCompetenciaForm(request.POST, instance=alumnoxcompetencia)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnoxcompetencia')
    else:
        form = AlumnosXCompetenciaForm(instance=alumnoxcompetencia)
    return render(request, 'modificar_alumnoxcompetencia.html', {'form': form, 'alumnoxcompetencia': alumnoxcompetencia})


def eliminar_alumnoxcompetencia(request, id_alumnos_competencia):
    alumnoxcompetencia = get_object_or_404(AlumnosXCompetencia, id_alumnos_competencia=id_alumnos_competencia)
    if request.method == 'POST':
        alumnoxcompetencia.delete()
    return redirect('lista_alumnoxcompetencia')

def lista_alumnoxcompetencia(request):
    alumnoxcompetencia = AlumnosXCompetencia.objects.all()
    return render(request, 'lista_alumnoxcompetencia.html', {'alumnoxcompetencia': alumnoxcompetencia})

## alumno x clase
def agregar_alumnoxclase(request):
    if request.method == 'POST':
        form = AlumnosXClaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnoxclase')
    else:
        form = AlumnosXClaseForm()
    return render(request, 'agregar_alumnoxclase.html', {'form': form})

def modificar_alumnoxclase(request, id_alumnos_clase):
    alumnoxclase = get_object_or_404(AlumnosXClase, id_alumnos_clase=id_alumnos_clase)
    if request.method == 'POST':
        form = AlumnosXClaseForm(request.POST, instance=alumnoxclase)
        if form.is_valid():
            form.save()
            return redirect('lista_alumnoxclase')
    else:
        form = AlumnosXClaseForm(instance=alumnoxclase)
    return render(request, 'modificar_alumnoxclase.html', {'form': form, 'alumnoxclase': alumnoxclase})


def eliminar_alumnoxclase(request, id_alumnos_clase):
    alumnoxclase = get_object_or_404(AlumnosXClase, id_alumnos_clase=id_alumnos_clase)
    if request.method == 'POST':
        alumnoxclase.delete()
    return redirect('lista_alumnoxclase')

def lista_alumnoxclase(request):
    alumnoxclase = AlumnosXClase.objects.all()
    return render(request, 'lista_alumnoxclase.html', {'alumnoxclase': alumnoxclase})

## estado de cuotas 


