from abc import abstractmethod
from django.db import models
import json

# Create your models here.

class Persona(models.Model):
    class Meta:
        abstract: True
    nombres = models.CharField(max_length=255)
    def __str__(self):
        pass
    @abstractmethod
    def getTipo(self):
        pass
    def getJSON(self):
        pass

class Cuenta(models.Model):
    usuario = models.CharField(max_length=255, unique=True)
    contrasenha = models.CharField(max_length=255)
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        blank=False,
        related_name="cuenta"
    )
    def __str__(self):
        return "Cuenta={usuario=" + self.usuario + "; contrasenha= " + self.contrasenha + "}"
    def getJSON(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "contrasenha": self.contrasenha
        }

class Estudiante(Persona):
    correo = models.CharField(max_length=255)
    def getTipo(self):
        return 1
    def __str__(self):
        return "Estudiante={nombres=" + self.nombres + "; correo=" + self.correo + "; cuenta=" + str(self.cuenta)
    def getJSON(self):
        return {
            "id": self.id,
            "nombres": self.nombres,
            "correo": self.correo
        }

class Administrador(Persona):
    celular = models.CharField(max_length=255)
    def getTipo(self):
        return 3
    def __str__(self):
        return "Administrador={nombres=" + self.nombres + "; celular=" + self.celular + "; cuenta=" + str(self.cuenta)
    def getJSON(self):
        return {
            "id": self.id,
            "nombres": self.nombres,
            "celular": self.celular
        }
        
class Profesor(Persona):
    foto = models.TextField()
    def __str__(self):
        return "Profesor={foto=" + self.foto + "}"

class Carrera(models.Model):
    nombre = models.CharField(max_length=255)

class Nivel(models.Model):
    numero = models.IntegerField()

class Curso(models.Model):
    nombre = models.IntegerField()
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, blank=False, related_name='cursos')
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, blank=False, related_name='cursos')
    def getJSON(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }

class Periodo(models.Model):
    codigo = models.IntegerField()

class Seccion(models.Model):
    codigo = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, blank=False, related_name='secciones')
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, blank=False, related_name='secciones')
    
class Asesoria(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    enlace = models.TextField()
    ambiente = models.TextField()
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, blank=False, related_name='asesorias')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, blank=False, related_name='asesorias')

class Reserva(models.Model):
    codigo = models.IntegerField()
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, blank=False, related_name='reservas')
    asesoria = models.ForeignKey(Asesoria, on_delete=models.CASCADE, blank=False, related_name='reservas')
    

'''
class Context():
    strategy :Persona
    def setStrategy(self, persona:Persona):
        self.strategy = persona
    def executeStrategy(self):
        self.strategy.getTipo()

class SingletonModel(models.Model):
    class Meta:
        abstract = True
    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(pk=1)
        return instance

class RegistroPersonas(SingletonModel):
    registro = models.JSONField(default=list)
    def agregar(self, p:Persona):
        self.registro.append(p)
    def imprimir(self):
        for r in self.registro:
            print(r)
    def getJSON(self):
        lista_serializable = [persona.getJSON() for persona in self.registro]
        return json.dumps(lista_serializable, ensure_ascii=False)
'''