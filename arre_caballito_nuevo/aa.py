import os
import django

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arre_caballito.settings')
django.setup()
import datetime
from datetime import date
from alumnos.models import Alumno, AlumnoClase  # Asegúrate de importar el modelo Alumno
from cuotas.models import Monto, Periodo

def imprimir_alumnos():
    """Imprime todos los alumnos registrados en la base de datos."""
    alumnos = AlumnoClase.objects.all()  # Obtiene todos los alumnos
    mes_actual = datetime.datetime.now().month
    anio_actual = datetime.datetime.now().year
    mes_actual = f"{mes_actual:02}"
    mes_actual = int(mes_actual)
    periodos = Periodo.objects.all()
    # Imprime cada alumno
    print(mes_actual)
    for alumno in alumnos:
        print("")
        for mes in range(mes_actual, 13):
            print("")
            print(f"Alumno: {alumno.alumno.id_alumno}")
            a = f"{mes:02}"
            asd = Periodo.objects.filter(mes=a, anio=anio_actual).first()
            print(asd)
            disciplina = alumno.clase.id_disciplina.nombre
            print(disciplina)
            monto = Monto.objects.filter(disciplina=alumno.clase.id_disciplina).first()
            print(monto.monto)
            fecha_vencimiento = date(anio_actual, mes, 10)
            print(fecha_vencimiento)
            detalle = alumno.clase.id_clase
            print(detalle)

            if mes > datetime.datetime.now().month:
                estado = 'Próximo'
            elif fecha_vencimiento > date.today():
                estado = 'Pendiente'
            else:
                estado = 'Vencido'
            print(estado)
            
            
        
if __name__ == "__main__":
    # Imprimir todos los alumnos
    imprimir_alumnos()
