from unidecode import unidecode
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
from app.models import *

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
    def subir(df, periodo, fecha_comienzo):
        
        periodo, _ = Periodo.objects.get_or_create(codigo="2024 - 1")

        for indice_fila, fila in df.iterrows():
            
            carrera = 'Ingenieria de sistemas'
            carrera, _ = Carrera.objects.get_or_create(nombre=carrera)

            nivel = int(fila['Nivel'])
            n, _ = Nivel.objects.get_or_create(numero = nivel)

            curso_codigo = fila['COD']
            curso_nombre = fila['NOMBRE CURSO_AUX']
            c, _ = Curso.objects.get_or_create(codigo=curso_codigo, nombre=curso_nombre, nivel=n, carrera=carrera)

            profesor_nombre = fila['PROFESOR TITULAR']
            #profesor_foto = GestionarImagenes.obtener_url_segunda_imagen_google(profesor_nombre)
            p, _ = Profesor.objects.get_or_create(nombres=profesor_nombre)

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

