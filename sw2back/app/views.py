from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from app.models import *
#from sw2back.app.clases.patrones import *
#from sw2back.app.clases.seeders import *
from datetime import datetime


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

class GestionPersonas:

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
    def profesor(request):

        r = DecoratorProfesorId(RequestExtractor(request))
        [profesor_id] = r.extract()

        profesor = Profesor.objects.filter(id=profesor_id).first()

        if not profesor:
            return HttpResponseBadRequest("profesor inexistente")
        
        return JsonResponse(profesor.getAsesorias(), safe=False)

class GestionAsesorias:
    
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
            return HttpResponseBadRequest("usted ya ha reservado esta asesoria")
        else:
            codigo = GestionAsesorias.generarCodigo()
            reserva = Reserva(codigo=codigo, estudiante=estudiante, asesoria=asesoria)
            reserva.save()
            return JsonResponse(reserva.getJSONSimple(), safe=False)
        

class GestionarAdministrador:
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
