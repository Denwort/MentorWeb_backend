from bs4 import BeautifulSoup
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.views.decorators.http import require_http_methods
import requests
import unidecode
from app.models import *
#from sw2back.app.clases.patrones import *
#from sw2back.app.clases.seeders import *
from datetime import datetime
import json
import pandas as pd
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
import random

class GestionCuentas:

    @require_http_methods(["POST"])
    def register(request):

        r = DecoratorUsuario(DecoratorContrasenha(DecoratorNombres(DecoratorCorreo(RequestExtractor(request)))))
        [usuario, contrasenha, nombres, correo] = r.extract()

        cuenta = Cuenta.objects.filter(usuario=usuario).exists()

        if cuenta:
            return HttpResponseBadRequest("usuario ya existe")
        else:
            estudiante = Estudiante.objects.filter(correo=correo).exists()
            if estudiante:
                return HttpResponseBadRequest("correo en uso")
            
            estudiante =  Estudiante(nombres=nombres, correo=correo)
            estudiante.save()
            cuenta = Cuenta(usuario=usuario, contrasenha=contrasenha, persona=estudiante)
            cuenta.save()

            return JsonResponse(cuenta.getJSONPersona(), safe=False)

    @require_http_methods(["POST"])
    def login(request):

        r = DecoratorUsuario(DecoratorContrasenha(RequestExtractor(request)))
        [usuario, contrasenha] = r.extract()

        cuenta = Cuenta.objects.filter(usuario=usuario).exists()
        if not cuenta:
            return HttpResponseBadRequest("Cuenta inexistente")
        
        cuenta = Cuenta.objects.filter(usuario=usuario, contrasenha=contrasenha).first()
        if not cuenta:
            return HttpResponseBadRequest("Contraseña incorrecta")
            
        return JsonResponse(cuenta.getJSONPersona(), safe=False)
    
    @require_http_methods(["POST"])
    def recuperarPregunta(request):
        r = DecoratorUsuario(DecoratorNombres(RequestExtractor(request)))
        [usuario, nombres] = r.extract()

        persona = get_object_or_404(Persona,nombres=nombres)
        #persona = Persona.objects.filter(nombres=nombres).exists()
        #if not persona:
        #    return HttpResponseBadRequest("No existe la persona")
        
        cuenta = get_object_or_404(Cuenta,usuario=usuario, persona=persona)
        #cuenta = Cuenta.objects.filter(usuario=usuario, persona=persona).first()
        #if not cuenta:
        #    return HttpResponseBadRequest("Contraseña incorrecta")
            
        return JsonResponse(cuenta.getJSONPregunta(), safe=False)

    @require_http_methods(["POST"])
    def recuperarRespuesta(request):
        r = DecoratorUsuario(DecoratorRespuesta(RequestExtractor(request)))
        [usuario,respuesta] = r.extract()
        
        cuenta = get_object_or_404(Cuenta,usuario=usuario, respuesta=respuesta)
            
        return JsonResponse(cuenta.getJSONPregunta(), safe=False)
    
    @require_http_methods(["POST"])
    def recuperarContrasenha(request):
        r = DecoratorUsuario(DecoratorNuevaContrasenia(RequestExtractor(request)))
        [usuario,nuevaContrasenia] = r.extract()

        cuenta = get_object_or_404(Cuenta,usuario=usuario)
        cuenta.contrasenha = nuevaContrasenia
        cuenta.save()
        
        return JsonResponse(cuenta.getJSONPregunta(), safe=False)

    @require_http_methods(["POST"])
    def verPerfil(request):
        r = DecoratorCuentaId(RequestExtractor(request))
        [cuenta_id] = r.extract()

        cuenta = get_object_or_404(Cuenta,id=cuenta_id)
        
        return JsonResponse(cuenta.getJSONTodo(), safe=False)
    
    @require_http_methods(["POST"])
    def preguntasDeSeguridad(request):

        preguntas = PreguntaDeSeguridad.objects.all()
        
        return JsonResponse([pregunta.getJSONSimple() for pregunta in preguntas], safe=False)

    @require_http_methods(["POST"])
    def editarPerfilEstudiante(request):
        
        cuenta_id = request.POST.get('cuenta_id')
        usuario = request.POST.get('usuario')
        contrasenha = request.POST.get('contrasenha')
        pregunta_id = request.POST.get('pregunta_id')
        respuesta = request.POST.get('respuesta')

        nombres = request.POST.get('nombres')
        correo = request.POST.get('correo')
        foto =  request.FILES['foto'] if 'foto' in request.FILES else None

        cuenta = get_object_or_404(Cuenta,id=cuenta_id)
        cuenta.usuario = usuario
        cuenta.contrasenha = contrasenha
        pregunta = get_object_or_404(PreguntaDeSeguridad,id=pregunta_id)
        cuenta.pregunta = pregunta
        cuenta.respuesta = respuesta
        cuenta.save()

        persona = cuenta.persona.getPersona()
        persona.nombres = nombres
        persona.correo = correo
        if foto:
            persona.foto = foto
        persona.save()
        
        return JsonResponse(cuenta.getJSONTodo(), safe=False)
    
    @require_http_methods(["POST"])
    def crear_cuenta_profesor(request):

        data_json = json.loads(request.body.decode('utf-8'))
        correo = data_json['correo']

        profesor = get_object_or_404(Profesor, correo=correo)
        nueva_contrasenha = ''.join(random.choice('0123456789') for _ in range(8))

        cuenta = Cuenta.objects.filter(persona=profesor).exists()
        if cuenta:
            return HttpResponseBadRequest('profesor ya registrado')

        cuenta = Cuenta.objects.create(persona_id=profesor.id, usuario=profesor.correo, contrasenha=nueva_contrasenha, pregunta_id=2, respuesta="2000")

        subject = 'Bienvenido a MentorWeb!'
        message = f'Hola {profesor.nombres}, gracias por registrarte en MentorWeb.\nAqui estan tus credenciales para la plataforma\nUsuario: {profesor.correo}\nContraseña: {nueva_contrasenha}\nDentro de la plataforma, en el apartado de perfil, podrás personalizar tus datos. Se le recomienda cambiar su contraseña inicial por una más segura.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [profesor.correo, ]
        send_mail( subject, message, email_from, recipient_list )

        return JsonResponse({"mensaje": "Las credenciales han sido enviadas a su correo"}, safe=False)
    
    @require_http_methods(["POST"])
    def editarPerfilProfesor(request):
        
        cuenta_id = request.POST.get('cuenta_id')
        usuario = request.POST.get('usuario')
        contrasenha = request.POST.get('contrasenha')
        pregunta_id = request.POST.get('pregunta_id')
        respuesta = request.POST.get('respuesta')

        nombres = request.POST.get('nombres')
        foto =  request.FILES['foto'] if 'foto' in request.FILES else None

        cuenta = get_object_or_404(Cuenta,id=cuenta_id)
        cuenta.usuario = usuario
        cuenta.contrasenha = contrasenha
        pregunta = get_object_or_404(PreguntaDeSeguridad,id=pregunta_id)
        cuenta.pregunta = pregunta
        cuenta.respuesta = respuesta
        cuenta.save()

        persona = cuenta.persona.getPersona()
        persona.nombres = nombres
        if foto:
            persona.foto = foto
        persona.save()
        
        return JsonResponse(cuenta.getJSONTodo(), safe=False)

class GestionAsesorias:
    
    @require_http_methods(["POST"])
    def asesorias_estudiante(request):

        r = DecoratorEstudianteId(RequestExtractor(request))
        [estudiante_id] = r.extract()

        estudiante = Estudiante.objects.filter(id=estudiante_id).first()
        
        if not estudiante:
            return HttpResponseBadRequest("estudiante inexistente")
        
        return JsonResponse(estudiante.getReservas(), safe=False)

    @require_http_methods(["POST"])
    def profesores(request):

        r = DecoratorKeyword(RequestExtractor(request))
        [keyword] = r.extract()

        profesores = Profesor.objects.filter(nombres__icontains=keyword)
        
        return JsonResponse([profesor.getJSONSimple() for profesor in profesores], safe=False)

    @require_http_methods(["POST"])
    def profesoresCliff(request):
        data_json = json.loads(request.body.decode('utf-8'))
        keywords_profesores = data_json['profesor']
        keywords_cursos = data_json['cursos']
        
        secciones_disponibles = Seccion.objects.all()

        secciones_filtradas = []

        for seccion in secciones_disponibles:
            profesor = seccion.profesor
            if any(keyword.lower() in profesor.nombres.lower() for keyword in keywords_profesores):
                curso = seccion.curso
                if any(keyword.lower() in curso.nombre.lower() for keyword in keywords_cursos):
                    secciones_filtradas.append(seccion.getJSONDerecha())
        
        if not secciones_filtradas:
            return JsonResponse({"error": "No se encontraron secciones para los keywords proporcionados"}, status=404)

        return JsonResponse(secciones_filtradas, safe=False)

    @require_http_methods(["POST"])
    def profesor(request):
        r = DecoratorProfesorId(RequestExtractor(request))
        [profesor_id] = r.extract()

        profesor = Profesor.objects.filter(id=profesor_id).first()

        if not profesor:
            return HttpResponseBadRequest("profesor inexistente")
        
        return JsonResponse(profesor.getAsesorias(), safe=False)
    
    @require_http_methods(["POST"])
    def profesorAsesoriasxd(request):
        r = DecoratorEstudianteId(DecoratorProfesorId(RequestExtractor(request)))
        [estudiante_id,profesor_id] = r.extract()

        profesor = Profesor.objects.filter(id=profesor_id).first()
        reservas = Reserva.objects.filter(estudiante_id=estudiante_id)

        if not profesor:
            return HttpResponseBadRequest("profesor inexistente")
        
        
        
        return JsonResponse(profesor.getAsesoriasConReserva(estudiante_id), safe=False)
    
    
    #obtengo profesor y usuario id
    #buscar si ya esta reservado con el usuario id
    #si el usuario ya reservo devuevlo un listado de que ya esta reservado
    #en caso contrario se manda la lista
    
    @require_http_methods(["POST"])
    def profesoresCursos(request):

        r = DecoratorFiltro(DecoratorKeyword(RequestExtractor(request)))
        [cursoId,keyword] = r.extract()

        profesores = Profesor.objects.filter(nombres__icontains=keyword)
        
        secciones = Seccion.objects.filter(curso=cursoId)
        profesor_ids = [seccion.profesor.id for seccion in secciones]
        
        profesores_filtrados = profesores.filter(id__in=profesor_ids)
        
        return JsonResponse([profesor.getJSONSimple() for profesor in profesores_filtrados], safe=False)

    @staticmethod
    def generarCodigo():
        timestamp = datetime.now().timestamp()
        unique_code = int(timestamp)
        return unique_code

    @require_http_methods(["POST"])
    def reservar(request):

        r = DecoratorEstudianteId(DecoratorAsesoriaId(RequestExtractor(request)))
        [estudiante_id, asesoria_id] = r.extract()

        estudiante = Estudiante.objects.filter(id=estudiante_id).first()

        if not estudiante:
            return HttpResponseBadRequest("estudiante inexistente")
        
        asesoria = Asesoria.objects.filter(id=asesoria_id).first()

        if not asesoria:
            return HttpResponseBadRequest("reserva inexistente")

        creado = Reserva.objects.filter(estudiante=estudiante, asesoria=asesoria).exists()
        if creado:
            return HttpResponseBadRequest("Usted ya ha reservado esta asesoria")
        else:
            codigo = GestionAsesorias.generarCodigo()
            reserva = Reserva(codigo=codigo, estudiante=estudiante, asesoria=asesoria)
            reserva.save()
            return JsonResponse(reserva.getJSONSimple(), safe=False)
        
    @require_http_methods(["POST"])
    def reservarEliminar(request):

        r = DecoratorReservaId(RequestExtractor(request))
        [reserva_id] = r.extract()

        reserva = Reserva.objects.filter(id=reserva_id).first()
        if reserva:
            reserva.delete()
            return JsonResponse({'message': 'Reserva eliminada exitosamente'}, safe=False)
        else:
            return HttpResponseBadRequest("Reserva no encontrada")

    @require_http_methods(["POST"])
    def abrir_extra(request):

        data_json = json.loads(request.body.decode('utf-8'))
        seccion_id = data_json['seccion_id']
        fecha_inicio = data_json['fecha_inicio']
        fecha_fin = data_json['fecha_fin']
        enlace = data_json['enlace']
        ambiente = data_json['ambiente']

        asesoria = Asesoria.objects.create(seccion_id=seccion_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, enlace=enlace, ambiente=ambiente, extra=True)

        return JsonResponse(asesoria.getJSONSimple(), safe=False)

    @require_http_methods(["POST"])
    def listar_extras(request):
        data_json = json.loads(request.body.decode('utf-8'))
        profesor_id = data_json['profesor_id']
        profesor = get_object_or_404(Profesor, id=profesor_id)
        return JsonResponse(profesor.getAsesoriasExtra(), safe=False)

    @require_http_methods(["POST"])
    def cerrar_extra(request):
        data_json = json.loads(request.body.decode('utf-8'))
        asesoria_id = data_json['asesoria_id']
        asesoria = get_object_or_404(Asesoria, id=asesoria_id)
        if(asesoria.extra == True):
            asesoria.delete()
        return JsonResponse({'message': 'Reserva eliminada exitosamente'}, safe=False)

    @require_http_methods(["POST"])
    def profesor_listar_asesorias(request):

        data_json = json.loads(request.body.decode('utf-8'))
        profesor_id = data_json['profesor_id']

        profesor = get_object_or_404(Profesor, id=profesor_id)
        
        return JsonResponse(profesor.getReservaciones(), safe=False)
        
class GestionAdministrador:
    @require_http_methods(["POST"])
    def cargar(request):
        
        periodo = request.POST.get('periodo')
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')

        excel_secciones = request.FILES['excel_secciones']
        excel_asesorias = request.FILES['excel_asesorias']
        df = GestionarInformacion.leer(excel_secciones, excel_asesorias)

        
        GestionarInformacion.subir(df, periodo, fecha_inicio)

        df_json = df.to_dict(orient='records')
        return JsonResponse({'data': df_json}, json_dumps_params={'ensure_ascii': False})

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
        data_json = {}
        try:
            data_json = json.loads(self.request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise Http404("Error al procesar la solicitud")
        res = []
        for l in self.lista:
            try:
                res.append(data_json[l])
            except (KeyError, ValueError) as e:
                raise Http404("Falta la clave ${l} en la solicitud")       
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
class DecoratorRespuesta(Decorator):
    def extract(self):
        self.lista.append('respuesta')
        return self.component.extract()
class DecoratorNuevaContrasenia(Decorator):
    def extract(self):
        self.lista.append('nuevaContrasenia')
        return self.component.extract()
    
# Para el repositorio
class DecoratorCursoId(Decorator):
    def extract(self):
        self.lista.append('curso_id')
        return self.component.extract()
class DecoratorDocumentoId(Decorator):
    def extract(self):
        self.lista.append('documento_id')
        return self.component.extract()
class DecoratorPeriodoId(Decorator):
    def extract(self):
        self.lista.append('periodo_id')
        return self.component.extract()
class DecoratorTicketId(Decorator):
    def extract(self):
        self.lista.append('ticket_id')
        return self.component.extract()
class DecoratorNombre(Decorator):
    def extract(self):
        self.lista.append('nombre')
        return self.component.extract()
class DecoratorDescripcion(Decorator):
    def extract(self):
        self.lista.append('descripcion')
        return self.component.extract()
class DecoratorComentario(Decorator):
    def extract(self):
        self.lista.append('comentario')
        return self.component.extract()
class DecoratorCuentaId(Decorator):
    def extract(self):
        self.lista.append('cuenta_id')
        return self.component.extract()
class DecoratorFiltro(Decorator):
    def extract(self):
        self.lista.append('filtro')
        return self.component.extract()
class DecoratorPreguntaId(Decorator):
    def extract(self):
        self.lista.append('pregunta_id')
        return self.component.extract()
class DecoratorSeccionId(Decorator):
    def extract(self):
        self.lista.append('seccion_id')
        return self.component.extract()
class DecoratorReservaId(Decorator):
    def extract(self):
        self.lista.append('reserva_id')
        return self.component.extract()


class GestionarStrings:
    @staticmethod
    def partes_pertenecen(substring, string_grande):
        string_grande = unidecode(string_grande).replace("/", ".").replace(" ", ".")
        string_grande = unidecode(string_grande)
        partes = unidecode(substring).replace(" ", ".").replace("/", ".").split('.')
        for parte in partes:
            if parte not in string_grande:
                return False
        return True
    @staticmethod
    def es_substring(string, lista):
        for elemento in lista:
            if GestionarStrings.partes_pertenecen(string, elemento):
                return elemento
        return
    @staticmethod
    def obtener_url_imagen(query):
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

class GestionarInformacion:

    @staticmethod
    def leer(excel_secciones, excel_asesorias):

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
                profesor_foto = GestionarStrings.obtener_url_imagen(profesor_nombre)
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


# Sprint 2
class GestionRepositorio:

    @require_http_methods(["POST"])
    def recientes(request):
        r = DecoratorEstudianteId(RequestExtractor(request))
        [estudiante_id] = r.extract()

        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        historial = estudiante.historial.all().order_by('-fecha_revision')
        
        return JsonResponse([hist.documento.getJSONConSeccion() for hist in historial], safe=False)

    @require_http_methods(["POST"])
    def cursos(request):

        cursos = Curso.objects.all()
        
        return JsonResponse([curso.getJSONDerecha() for curso in cursos], safe=False)

    @require_http_methods(["POST"])
    def curso(request):

        r = DecoratorCursoId(RequestExtractor(request))
        [curso_id] = r.extract()

        curso = Curso.objects.filter(id=curso_id).first()

        if not curso:
            return HttpResponseBadRequest("curso inexistente")
        
        return JsonResponse(curso.getJSONDerecha(), safe=False)

    @require_http_methods(["POST"])
    def documentos(request):

        r = DecoratorCursoId(RequestExtractor(request))
        [curso_id] = r.extract()

        curso = get_object_or_404(Curso, id=curso_id)
        
        return JsonResponse(curso.getDocumentos(), safe=False)
    
    @require_http_methods(["POST"])
    def documento(request):

        r = DecoratorEstudianteId(DecoratorDocumentoId(RequestExtractor(request)))
        [estudiante_id, documento_id] = r.extract()

        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        documento = get_object_or_404(Documento, id=documento_id)

        limite = 10
        historial = Historial.objects.filter(estudiante_id=estudiante_id).order_by('-fecha_revision')
        if historial.count() > limite:
            for revision in historial[limite:]:
                revision.delete()
        if len(historial) == 0 or str(historial[0].documento_id) != documento_id:
            Historial.objects.create(estudiante=estudiante, documento=documento)
        
        return JsonResponse(documento.getJSONConSeccion(), safe=False)
    
class GestionTickets:
    
    @require_http_methods(["POST"])
    def obtener_periodos(request):
        periodos = Periodo.objects.all()
        return JsonResponse([periodo.getJSONSimple() for periodo in periodos], safe=False)
    
    @require_http_methods(["POST"])
    def obtener_cursos(request):
        cursos = Curso.objects.all()
        return JsonResponse([curso.getJSONDerecha() for curso in cursos], safe=False)

    @require_http_methods(["POST"])
    def buscar_seccion(request):

        r = DecoratorPeriodoId(DecoratorCursoId(RequestExtractor(request)))
        [periodo_id, curso_id] = r.extract()

        periodo = get_object_or_404(Periodo, id=periodo_id)
        curso = get_object_or_404(Curso, id=curso_id)

        secciones = Seccion.objects.filter(periodo=periodo, curso=curso)

        return JsonResponse([seccion.getJSONConProfesor() for seccion in secciones], safe=False)
    
    @require_http_methods(["POST"])
    def crear(request):

        estudiante_id = request.POST.get('estudiante_id')
        seccion_id = request.POST.get('seccion_id')

        asunto = request.POST.get('asunto')
        comentario = request.POST.get('comentario')
        descripcion = request.POST.get('descripcion')
        estado = "Pendiente"
        archivo = request.FILES['archivo']

        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        seccion = get_object_or_404(Seccion, id=seccion_id)

        ticket = Ticket(asunto=asunto, comentario=comentario, descripcion=descripcion, estado=estado, archivo=archivo, estudiante=estudiante, seccion=seccion)
        ticket.save()
        
        return JsonResponse(ticket.getJSONSimple(), safe=False)
    
    @require_http_methods(["POST"])
    def tickets_todos(request):

        tickets = Ticket.objects.all()

        return JsonResponse([ticket.getJSONCompleto() for ticket in tickets], safe=False)
    

    @require_http_methods(["POST"])
    def pendientes(request):

        tickets = Ticket.objects.filter(estado="Pendiente")

        return JsonResponse([ticket.getJSONCompleto() for ticket in tickets], safe=False)
    
    @require_http_methods(["POST"])
    def ticket(request):
        r = DecoratorTicketId(RequestExtractor(request))
        [ticket_id] = r.extract()

        ticket = get_object_or_404(Ticket, id=ticket_id)

        return JsonResponse(ticket.getJSONCompleto(), safe=False)

    @require_http_methods(["POST"])
    def aceptar(request):
        r = DecoratorTicketId(DecoratorComentario(DecoratorNombre(DecoratorDescripcion(RequestExtractor(request)))))
        [ticket_id, comentario, nombre, descripcion] = r.extract()

        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.estado = "Aceptado"
        ticket.comentario = comentario
        ticket.asunto = nombre
        ticket.descripcion = descripcion
        ticket.save()
        
        archivo = ticket.archivo
        seccion = ticket.seccion

        documento = Documento(nombre=nombre, descripcion=descripcion, archivo=archivo, seccion=seccion)
        documento.save()

        return JsonResponse(documento.getJSONSimple(), safe=False)
    
    @require_http_methods(["POST"])
    def rechazar(request):
        r = DecoratorTicketId(DecoratorComentario(RequestExtractor(request)))
        [ticket_id, comentario] = r.extract()

        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.estado = "Rechazado"
        ticket.comentario = comentario
        ticket.save()

        return JsonResponse(ticket.getJSONCompleto(), safe=False)
    
    @require_http_methods(["POST"])
    def tickets(request):
        r = DecoratorEstudianteId(RequestExtractor(request))
        [estudiante_id] = r.extract()

        tickets = Ticket.objects.filter(estudiante_id = estudiante_id)

        return JsonResponse([ticket.getJSONCompleto() for ticket in tickets], safe=False)