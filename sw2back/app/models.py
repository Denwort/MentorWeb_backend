from __future__ import annotations
from abc import ABC, abstractmethod
from django.db import models
import json
from unidecode import unidecode
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Create your models here.

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
                (asesoria.getFecha() >= fecha_actual)]
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



# Patrones.py

# Patron Decorator

class Extractor():
    lista = []
    def extract(self):
        pass

class RequestExtractor(Extractor):
    def __init__(self, request):
        self.lista.clear()
        self.request = request
    def extract(self):
        data_json = json.loads(self.request.body.decode('utf-8'))
        res = []
        for l in self.lista:
            res.append(data_json[l])            
        return res

class Decorator(Extractor):
    _component: Extractor = None

    def __init__(self, component: Extractor):
        self._component = component

    @property
    def component(self) -> Extractor:
        return self._component

    def extract(self):
        return self._component.extract()

class DecoratorUsuario(Decorator):
    def extract(self):
        self.lista.append('usuario')
        return self.component.extract()
class DecoratorContrasenha(Decorator):
    def extract(self):
        self.lista.append('contrasenha')
        return self.component.extract()
class DecoratorNombres(Decorator):
    def extract(self):
        self.lista.append('nombres')
        return self.component.extract()
class DecoratorCorreo(Decorator):
    def extract(self):
        self.lista.append('correo')
        return self.component.extract()

class DecoratorEstudianteId(Decorator):
    def extract(self):
        self.lista.append('estudiante_id')
        return self.component.extract()
class DecoratorProfesorId(Decorator):
    def extract(self):
        self.lista.append('profesor_id')
        return self.component.extract()
class DecoratorKeyword(Decorator):
    def extract(self):
        self.lista.append('keyword')
        return self.component.extract()
class DecoratorAsesoriaId(Decorator):
    def extract(self):
        self.lista.append('asesoria_id')
        return self.component.extract()

    

    
# Singleton para marcar el Periodo actual y la fecha actual
# Lo utiliza Estudiante y Profesor para obtener: reservas en el periodo actual y secciones en el periodo actual
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    periodoActual = "2024-1"
    def getPeriodoActual(self):
        return self.periodoActual
    def setPeriodoActual(self, nuevoPeriodo):
        self.periodoActual = nuevoPeriodo
    def getFechaActual(self):
        return datetime.now().replace(tzinfo=timezone.utc)

# Factory method para crear Cuentas y Personas


# Controlar el periodo actual












# Seeders


class GestionarStrings:
    @staticmethod
    def es_substring(string, lista):
        for elemento in lista:
            if GestionarStrings.partes_pertenecen(string, elemento):
                return elemento
        return
    @staticmethod
    def partes_pertenecen(substring, string_grande):
        string_grande = unidecode(string_grande).replace("/", ".").replace(" ", ".")
        string_grande = unidecode(string_grande)
        partes = unidecode(substring).replace(" ", ".").replace("/", ".").split('.')
        for parte in partes:
            if parte not in string_grande:
                return False
        return True

class GestionarFechas:
    @staticmethod
    def obtener_fecha(fecha_comienzo, numero_de_semana, dia_de_semana):
        semana_comienzo = fecha_comienzo.strftime("%W")
        numero_semana = int(semana_comienzo) + (numero_de_semana-1)
        año = fecha_comienzo.year
        dia_semana = dia_de_semana
        primer_dia_del_año = datetime(año, 1, 1)
        dias_para_dia_semana = (numero_semana - 1) * 7
        dia_deseado = primer_dia_del_año + timedelta(days=dias_para_dia_semana - primer_dia_del_año.weekday())
        if dia_semana.lower() == 'lunes':
            pass
        elif dia_semana.lower() == 'martes':
            dia_deseado += timedelta(days=1)
        elif dia_semana.lower() == 'miércoles':
            dia_deseado += timedelta(days=2)
        elif dia_semana.lower() == 'jueves':
            dia_deseado += timedelta(days=3)
        elif dia_semana.lower() == 'viernes':
            dia_deseado += timedelta(days=4)
        elif dia_semana.lower() == 'sábado':
            dia_deseado += timedelta(days=5)
        elif dia_semana.lower() == 'domingo':
            dia_deseado += timedelta(days=6)
        return dia_deseado
    @staticmethod
    def poner_hora(fecha, nueva_hora):
        fecha_actualizada = fecha.replace(hour=nueva_hora, minute=0, second=0, microsecond=0)
        return fecha_actualizada

class GestionarImagenes:
    @staticmethod
    def obtener_url_segunda_imagen_google(query):
        url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        respuesta = requests.get(url, headers=headers)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        miniaturas = soup.find_all("img")
        if len(miniaturas) >= 2:
            url_segunda_imagen = miniaturas[1]["src"]
            return url_segunda_imagen
        else:
            return "No se encontraron suficientes imágenes"
    
class GestionarInformacion:
    @staticmethod
    def leer(excel_secciones, excel_asesorias):

        #excel_secciones = '/content/2024-1_Horarios_Cursos_Sección.xlsx'
        #excel_asesorias = '/content/Atención_alumnos_2024-1.xlsx'

        df_secciones = pd.read_excel(excel_secciones)
        df_asesorias = pd.read_excel(excel_asesorias)

        df_secciones['NOMBRE CURSO_AUX'] = df_secciones['NOMBRE CURSO'].str.upper()
        df_asesorias['Asignatura_AUX'] = df_asesorias['Asignatura'].str.upper()

        df_secciones['PROFESOR TITULAR_AUX'] = df_secciones['PROFESOR TITULAR'].str.replace(',', '')

        with open('./app/files/cursos.txt', 'r', encoding='utf-8') as archivo:
            lineas = [linea.rstrip('\n') for linea in archivo.readlines()]

        lineas = [linea.strip() for linea in lineas]
        for i in df_asesorias['Asignatura_AUX']:
            concordancia = GestionarStrings.es_substring(i, lineas)
            if concordancia:
                df_asesorias.loc[df_asesorias['Asignatura_AUX'] == i, 'Asignatura_AUX'] = concordancia
            else:
                print("No encontrado: ", i)
        for i in df_secciones['NOMBRE CURSO_AUX']:
            concordancia = GestionarStrings.es_substring(i, lineas)
            if concordancia:
                df_secciones.loc[df_secciones['NOMBRE CURSO_AUX'] == i, 'NOMBRE CURSO_AUX'] = concordancia
            else:
                print("No encontrado: ", i)

        for i in df_secciones['PROFESOR TITULAR_AUX']:
            concordancia = GestionarStrings.es_substring(i, df_asesorias['Docente'])
            if concordancia:
                df_secciones.loc[df_secciones['PROFESOR TITULAR_AUX'] == i, 'PROFESOR TITULAR_AUX'] = concordancia
            else:
                print("No encontrado: ", i)

        df_secciones['Profesor_Curso'] = df_secciones['NOMBRE CURSO_AUX'] + ' - ' + df_secciones['PROFESOR TITULAR_AUX']
        df_asesorias['Profesor_Curso'] = df_asesorias['Asignatura_AUX'] + ' - ' + df_asesorias['Docente']

        df_merged = pd.merge(df_secciones, df_asesorias , on='Profesor_Curso', how='left')

        df_merged.drop(columns=['Asignatura_AUX', 'PROFESOR TITULAR_AUX', 'Profesor_Curso'], inplace=True)
        df_merged = df_merged.fillna('')

        return df_merged
    
    @staticmethod
    def subir(df, nuevo_periodo, fecha_comienzo):
        
        periodo, _ = Periodo.objects.get_or_create(codigo=nuevo_periodo)

        for indice_fila, fila in df.iterrows():
            
            carrera = 'Ingenieria de sistemas'
            carrera, _ = Carrera.objects.get_or_create(nombre=carrera)

            nivel = int(fila['Nivel'])
            n, _ = Nivel.objects.get_or_create(numero = nivel)

            curso_codigo = fila['COD']
            curso_nombre = fila['NOMBRE CURSO_AUX']
            c, _ = Curso.objects.get_or_create(codigo=curso_codigo, nombre=curso_nombre, nivel=n, carrera=carrera)

            profesor_nombre = fila['PROFESOR TITULAR']
            p, creado = Profesor.objects.get_or_create(nombres=profesor_nombre)
            if creado:
                profesor_foto = GestionarImagenes.obtener_url_segunda_imagen_google(profesor_nombre)
                p.foto = profesor_foto
                p.save()
                
            seccion_codigo = int(fila['Seccion'])
            s, _ = Seccion.objects.get_or_create(codigo=seccion_codigo, curso=c, periodo=periodo, profesor=p)
            print("Agregado: ", s)
            if fila['Día'] != '':
                for i in range(1,17):
                    fecha = GestionarFechas.obtener_fecha(fecha_comienzo, i, fila['Día'])
                    fecha_inicio = GestionarFechas.poner_hora(fecha, int(fila['Inicio']))
                    fecha_fin = GestionarFechas.poner_hora(fecha, int(fila['Fin']))
                    ambiente = fila['Ambientes']
                    enlace = fila['Enlace Virtual']
                    a, _ = Asesoria.objects.get_or_create(seccion=s, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, ambiente=ambiente, enlace=enlace)

