from __future__ import annotations
from abc import abstractmethod
from django.db import models
from app.patrones import Singleton
import json


# Create your models here.

class Persona(models.Model):
    class Meta:
        abstract: True
    nombres = models.CharField(max_length=255)
    # Faltaria cmabiar para utilizar Factory Method
    '''
    from abc import ABC, abstractmethod

    class PersonaManager(ABC):
        @abstractmethod
        def get_persona(self):
            pass

    class EstudianteManager(PersonaManager):
        def get_persona(self):
            return Estudiante.objects.get(pk=self.pk)

    class ProfesorManager(PersonaManager):
        def get_persona(self):
            return Profesor.objects.get(pk=self.pk)

    class Persona(models.Model):
        # Campos comunes a todas las personas

        objects = PersonaManager()

    class Estudiante(Persona):
        # Campos específicos de los estudiantes

    class Profesor(Persona):
        # Campos específicos de los profesores
    '''
    @property
    def tipo(self):
        if hasattr(self, 'estudiante'):
            return 'Estudiante'
        elif hasattr(self, 'administrador'):
            return 'Administrador'
        else:
            return 'Persona'
    def getPersona(self):
        if hasattr(self, 'estudiante'):
            return Estudiante.objects.get(pk=self.pk)
        if hasattr(self, 'administrador'):
            return Administrador.objects.get(pk=self.pk)
    def __str__(self):
        pass
    @abstractmethod
    def getJSONSimple(self):
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
    def getJSONPersona(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "contrasenha": self.contrasenha,
            "persona": self.persona.getPersona().getJSONSimple()
        }

class Estudiante(Persona):
    correo = models.CharField(max_length=255)
    def getTipo(self):
        return "Estudiante"
    def __str__(self):
        return "Estudiante={nombres=" + self.nombres + "; correo=" + self.correo + "; cuenta=" + str(self.cuenta)
    def getJSONSimple(self):
        return {
            "id": self.id,
            "tipo": self.getTipo(),
            "nombres": self.nombres,
            "correo": self.correo
        }
    def getReservas(self):
        s = Singleton()
        periodo_actual = s.getPeriodoActual()
        fecha_actual = s.getFechaActual()
        return [reserva.getJSONAsesoria() for reserva in self.reservas.all() if 
                (reserva.getPeriodo() == periodo_actual and reserva.getFecha() >= fecha_actual)]

class Administrador(Persona):
    celular = models.CharField(max_length=255)
    def getTipo(self):
        return "Administrador"
    def __str__(self):
        return "Administrador={nombres=" + self.nombres + "; celular=" + self.celular + "; cuenta=" + str(self.cuenta)
    def getJSONSimple(self):
        return {
            "id": self.id,
            "tipo": self.getTipo(),
            "nombres": self.nombres,
            "celular": self.celular
        }
        
class Profesor(Persona):
    foto = models.TextField()
    def getTipo(self):
        return "Profesor"
    def __str__(self):
        return "Profesor={foto=" + self.foto + "}"
    def getJSON(self):
        return {
            "id": self.id,
            "nombres": self.nombres,
            "foto": self.foto,
            "secciones": self.secciones.getJSON()
        }
    def getJSONSimple(self):
        return {
            "id": self.id,
            "nombres": self.nombres,
            "foto": self.foto,
        }
    def getAsesorias(self):
        s = Singleton()
        periodo_actual = s.getPeriodoActual()
        return {
            "id": self.id,
            "nombres": self.nombres,
            "foto": self.foto,
            "secciones": [seccion.getJSONArriba() for seccion in self.secciones.all() if seccion.getPeriodo() == periodo_actual]
        }
    
class Carrera(models.Model):
    nombre = models.CharField(max_length=255)
    def getJSONSimple(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }

class Nivel(models.Model):
    numero = models.IntegerField()
    def getJSONSimple(self):
        return {
            "id": self.id,
            "numero": self.numero
        }

class Curso(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=255)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, blank=False, related_name='cursos')
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, blank=False, related_name='cursos')
    def getCarrera(self):
        return self.carrera.getNombre()
    def getJSON(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "carrera": self.carrera,
            "nivel": self.nivel
        }
    def getJSONDerecha(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "carrera": self.carrera.getJSONSimple(),
            "nivel": self.nivel.getJSONSimple()
        }

class Periodo(models.Model):
    codigo = models.CharField(max_length=255, unique=True)
    def getJSONSimple(self):
        return {
            "id": self.id,
            "codigo": self.codigo
        }
    def getPeriodo(self):
        return self.codigo
   
class Seccion(models.Model):
    codigo = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, blank=False, related_name='secciones')
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, blank=False, related_name='secciones')
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, blank=False, related_name='secciones')
    def __str__(self):
        return "Seccion={codigo=" + str(self.codigo) + "}"
    def getJSON(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "curso": self.curso.getJSON(),
            "periodo": self.periodo.getJSON(),
            "profesor": self.profesor.getJSON(),
        }
    def getJSONDerecha(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "curso": self.curso.getJSONDerecha(),
            "periodo": self.periodo.getJSONSimple(),
            "profesor": self.profesor.getJSONSimple(),
        }
    def getJSONArriba(self):
        s = Singleton()
        fecha_actual = s.getFechaActual()
        return {
            "id": self.id,
            "codigo": self.codigo,
            "curso": self.curso.getJSONDerecha(),
            "periodo": self.periodo.getJSONSimple(),
            "asesorias": [asesoria.getJSONSimple() for asesoria in self.asesorias.all() if 
                (asesoria.seccion == self and asesoria.getFecha() >= fecha_actual)]
        }
    def getPeriodo(self):
        return self.periodo.getPeriodo()

 
class Asesoria(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    enlace = models.TextField()
    ambiente = models.CharField(max_length=255)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, blank=False, related_name='asesorias')
    estudiantes = models.ManyToManyField(Estudiante, through='Reserva')
    def getJSON(self):
        return {
            "id": self.id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "enlace": self.enlace,
            "ambiente": self.ambiente,
            "seccion": self.seccion.getJSON(),
            "reservas": self.reservas.getJSON(),
        }
    def getJSONSimple(self):
        return {
            "id": self.id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "enlace": self.enlace,
            "ambiente": self.ambiente
        }
    def getJSONDerecha(self):
        return {
            "id": self.id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "enlace": self.enlace,
            "ambiente": self.ambiente,
            "seccion": self.seccion.getJSONDerecha(),
        }
    def getEstudiantes(self):
        return [estudiante.getJSON() for estudiante in self.estudiantes.all()]
    def getPeriodo(self):
        return self.seccion.getPeriodo()
    def getFecha(self):
        return self.fecha_fin
    

class Reserva(models.Model):
    codigo = models.IntegerField()
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, blank=False, related_name='reservas')
    asesoria = models.ForeignKey(Asesoria, on_delete=models.CASCADE, blank=False, related_name='reservas')
    def getJSONSimple(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "estudiante": self.estudiante.getJSONSimple(),
            "asesoria": self.asesoria.getJSONSimple(),
        }
    def getJSONAsesoria(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "asesoria": self.asesoria.getJSONDerecha()
        }
    def getPeriodo(self):
        return self.asesoria.getPeriodo()
    def getFecha(self):
        return self.asesoria.getFecha()
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
