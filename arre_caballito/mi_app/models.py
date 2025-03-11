from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Alumnos(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=9, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Competencia(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return self.nombre

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=9, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Clase(models.Model):
    id_clase = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.categoria} - {self.profesor}"
    
class Turno(models.Model):
    id_turno = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.categoria} - {self.hora_inicio} a {self.hora_fin}"

class Cuota(models.Model):
    id_cuota = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()

    def __str__(self):
        return f"Cuota {self.mes} - {self.alumno}"

class Caballo(models.Model):
    id_caballo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Macho'), ('H', 'Hembra')])

    def __str__(self):
        return self.nombre

class Montura(models.Model):
    id_montura = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.alumno} - {self.caballo}"

class Raza(models.Model):
    id_raza = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class AlumnosXCompetencia(models.Model):
    id_alumnos_competencia = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.alumno} - {self.competencia}"


class AlumnosXClase(models.Model):
    id_alumnos_clase = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.alumno} - {self.clase}"


class CaballoXRaza(models.Model):
    id_caballo_x_raza = models.AutoField(primary_key=True)
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE)
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.caballo} - {self.raza}"


class CaballoXDisciplina(models.Model):
    id_caballo_x_disciplina = models.AutoField(primary_key=True)
    caballo = models.ForeignKey(Caballo, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.caballo} - {self.disciplina}"

