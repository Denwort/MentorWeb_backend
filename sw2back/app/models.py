from __future__ import annotations
from abc import ABC, abstractmethod
from django.db import models
from datetime import datetime, timedelta, timezone
import uuid 

# Interfaces
class PeriodoInterface:
    @abstractmethod
    def getPeriodo(self):
        pass
class FechaInterface:
    @abstractmethod
    def getFecha(self):
        pass

# Modelos
class Persona(models.Model):
    class Meta:
        abstract: True
    nombres = models.CharField(max_length=255)
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
    @abstractmethod
    def getJSONSimple(self):
        pass

class PreguntaDeSeguridad(models.Model):
    texto=models.CharField(max_length=255)
    def getJSONSimple(self):
        return {
            "id": self.id,
            "texto": self.texto,
        }
    @staticmethod
    def get_default_pregunta():
        return 1

class Cuenta(models.Model):
    usuario = models.CharField(max_length=255, unique=True)
    contrasenha = models.CharField(max_length=255)
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        blank=False,
        related_name="cuenta"
    )
    pregunta = models.ForeignKey(PreguntaDeSeguridad, on_delete=models.CASCADE, blank=False,default=PreguntaDeSeguridad.get_default_pregunta(), related_name='cuentas')
    respuesta = models.CharField(max_length=255,default="nina")
    def getJSONPersona(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "contrasenha": self.contrasenha,
            "persona": self.persona.getPersona().getJSONSimple()
        }
    def getJSONPregunta(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "contrasenha": self.contrasenha,
            "pregunta": self.pregunta.getJSONSimple()
        }
    def getJSONTodo(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "contrasenha": self.contrasenha,
            "pregunta": self.pregunta.getJSONSimple(),
            "respuesta": self.respuesta,
            "persona": self.persona.getPersona().getJSONSimple()
        }

class Estudiante(Persona):
    correo = models.CharField(max_length=255, unique=False)
    foto = models.FileField(upload_to="imagenes/", default="imagenes/foto_default.png")
    def getJSONSimple(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nombres": self.nombres,
            "correo": self.correo,
            "foto": "http://127.0.0.1:8000"+self.foto.url
        }
    def getReservas(self):
        return [reserva.getJSONAsesoria() for reserva in self.reservas.all() if 
                (reserva.enPeriodoActual() and reserva.mayorAFechaActual())]

class Administrador(Persona):
    celular = models.CharField(max_length=255)
    def getJSONSimple(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nombres": self.nombres,
            "celular": self.celular
        }
        
class Profesor(Persona):
    foto = models.TextField()
    def getJSONSimple(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nombres": self.nombres,
            "foto": self.foto,
        }
    def getAsesorias(self):
        return {
            "id": self.id,
            "nombres": self.nombres,
            "foto": self.foto,
            "secciones": [seccion.getJSONArriba() for seccion in self.secciones.all() if seccion.enPeriodoActual()]
        }
    def getReservaciones(self):
        return [seccion.getJSONReservas() for seccion in self.secciones.all() if seccion.enPeriodoActual()]
    
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
    def getJSONDerecha(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "carrera": self.carrera.getJSONSimple(),
            "nivel": self.nivel.getJSONSimple()
        }
    def getDocumentos(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "carrera": self.carrera.getJSONSimple(),
            "nivel": self.nivel.getJSONSimple(),
            "secciones": [seccion.getDocumentos() for seccion in self.secciones.all()]
        } 

class Periodo(models.Model, PeriodoInterface):
    codigo = models.CharField(max_length=255, unique=True)
    def getJSONSimple(self):
        return {
            "id": self.id,
            "codigo": self.codigo
        }
    def enPeriodoActual(self):
        s = Singleton.load()
        periodo_actual = s.getPeriodoActual()
        return self.codigo == periodo_actual
   
class Seccion(models.Model, PeriodoInterface):
    codigo = models.IntegerField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, blank=False, related_name='secciones')
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, blank=False, related_name='secciones')
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, blank=False, related_name='secciones')
    def getJSONConProfesor(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "profesor": self.profesor.getJSONSimple()
        }
    def getJSONDerecha(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "curso": self.curso.getJSONDerecha(),
            "periodo": self.periodo.getJSONSimple(),
            "profesor": self.profesor.getJSONSimple(),
        }
    def getJSONReservas(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "curso": self.curso.getJSONDerecha(),
            "periodo": self.periodo.getJSONSimple(),
            "asesorias": [asesoria.getJSONReservas() for asesoria in self.asesorias.all() if 
                (asesoria.mayorAFechaActual())]
        }
    def enPeriodoActual(self):
        return self.periodo.enPeriodoActual()
    def getDocumentos(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "periodo": self.periodo.getJSONSimple(),
            "profesor": self.profesor.getJSONSimple(),
            "documentos": [documento.getJSONSimple() for documento in self.documentos.all()]
        }

 
class Asesoria(models.Model, PeriodoInterface, FechaInterface):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    enlace = models.TextField()
    ambiente = models.CharField(max_length=255)
    extra = models.BooleanField(default=False)
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, blank=False, related_name='asesorias')
    estudiantes = models.ManyToManyField(Estudiante, through='Reserva')

    def getJSONSimple(self):
        return {
            "id": self.id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "enlace": self.enlace,
            "ambiente": self.ambiente,
            "extra" : self.extra
        }
    def getJSONDerecha(self):
        return {
            "id": self.id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "enlace": self.enlace,
            "ambiente": self.ambiente,
            "extra" : self.extra,
            "seccion": self.seccion.getJSONDerecha(),
        }
    def getJSONReservas(self):
        return {
            "id": self.id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "enlace": self.enlace,
            "ambiente": self.ambiente,
            "extra" : self.extra,
            "reservas": [reserva.getJSONEstudiante() for reserva in self.reservas.all()]
        }
    def enPeriodoActual(self):
        return self.seccion.enPeriodoActual()
    def mayorAFechaActual(self):
        s = Singleton.load()
        fecha_actual = s.getFechaActual()
        return self.fecha_fin >= fecha_actual

class Reserva(models.Model, PeriodoInterface, FechaInterface):
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
    def getJSONEstudiante(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "estudiante": self.estudiante.getJSONSimple()
        }
    def enPeriodoActual(self):
        return self.asesoria.enPeriodoActual()
    def mayorAFechaActual(self):
        return self.asesoria.mayorAFechaActual()

# Singleton para marcar el Periodo actual y la fecha actual
    
class SingletonModel(models.Model):
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Singleton(SingletonModel):
    periodoActual = models.CharField(max_length=255)
    def getPeriodoActual(self):
        return self.periodoActual
    def setPeriodoActual(self, nuevoPeriodo):
        self.periodoActual = nuevoPeriodo
    def getFechaActual(self):
        return datetime.now().replace(tzinfo=timezone.utc)

# Sprint 2

class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to="archivos/")
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, blank=False, related_name='documentos')
    def getJSONSimple(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "archivo": self.archivo.url
        }
    def getJSONConSeccion(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "archivo": self.archivo.url,
            "seccion": self.seccion.getJSONDerecha()
        }

class Ticket(models.Model):
    def generar_nombre_unico(instance, filename):
        ext = filename.split('.')[-1]  # Obtener la extensión del archivo
        nombre_archivo = f"{uuid.uuid4().hex}.{ext}"  # Generar un nombre único usando UUID
        return f"archivos/{nombre_archivo}"
    asunto = models.CharField(max_length=255)
    descripcion = models.TextField()
    comentario = models.TextField()
    archivo = models.FileField(upload_to=generar_nombre_unico)
    estado = models.CharField(max_length=255, default="Pendiente")
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, blank=False, related_name='tickets')
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, blank=False, related_name='tickets')
    
    def getJSONSimple(self):
        return {
            "id": self.id,
            "asunto": self.asunto,
            "descripcion": self.descripcion,
            "comentario": self.comentario,
            "archivo": self.archivo.url,
            "estado": self.estado
        }
    def getJSONCompleto(self):
        return {
            "id": self.id,
            "asunto": self.asunto,
            "descripcion": self.descripcion,
            "comentario": self.comentario,
            "archivo": self.archivo.url,
            "estado": self.estado,
            "estudiante": self.estudiante.getJSONSimple(),
            "seccion": self.seccion.getJSONDerecha()
        }
    
class Historial(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, blank=False, related_name='historial')
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, blank=False, related_name='historial')
    fecha_revision = models.DateTimeField(auto_now_add=True)
    
