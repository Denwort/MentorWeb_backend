from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
from app.models import *
from datetime import datetime

# Create your views here.
@require_http_methods(["POST"])
def register(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    username = data_json['usuario']
    password = data_json['contrasenha']
    names = data_json['nombres']
    email = data_json['correo']

    cuenta = Cuenta.objects.filter(usuario=username).exists()
    if cuenta:
        return HttpResponseBadRequest("usuario ya existe")
    else:
        estudiante =  Estudiante(nombres=names, correo=email)
        estudiante.save()
        cuenta = Cuenta(usuario=username, contrasenha=password, persona=estudiante)
        cuenta.save()
        return JsonResponse({
            "tipo": estudiante.getTipo(),
            "mensaje": "Cuenta creada correctamente"
        })

@require_http_methods(["POST"])
def login(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    username = data_json['usuario']
    password = data_json['contrasenha']
    cuenta = Cuenta.objects.filter(usuario=username).exists()

    if not cuenta:
        return HttpResponseBadRequest("Cuenta inexistente")
    
    cuenta = Cuenta.objects.filter(usuario=username, contrasenha=password).exists()

    if not cuenta:
        return HttpResponseBadRequest("Contraseña incorrecta")
        
    cuenta = Cuenta.objects.filter(usuario=username, contrasenha=password).first()
    persona = cuenta.persona
    if hasattr(persona, 'estudiante'):
        estudiante = Estudiante.objects.filter(cuenta=cuenta).first()
        return JsonResponse({
            "tipo":estudiante.getTipo(),
            "cuenta": cuenta.getJSON(),
            "estudiante": estudiante.getJSON(),
            "mensaje": "Login exitoso"
        })
    if hasattr(persona, 'administrador'):
        administrador = Administrador.objects.filter(cuenta=cuenta).first()
        return JsonResponse({
            "tipo":administrador.getTipo(),
            "cuenta": cuenta.getJSON(),
            "administrador": administrador.getJSON(),
            "mensaje": "Login exitoso"
        })

@require_http_methods(["GET"])
def asesorias_estudiante(request):
    data_json = json.loads(request.body.decode('utf-8'))
    estudiante_id = data_json['estudiante_id']

    estudiante = Estudiante.objects.filter(id=estudiante_id).first()
    if not estudiante:
        return HttpResponseBadRequest("estudiante inexistente")
    
    return JsonResponse(estudiante.getReservas(), safe=False)

@require_http_methods(["GET"])
def profesores(request):
    data_json = json.loads(request.body.decode('utf-8'))
    keyword = data_json['keyword']
    profesores = Profesor.objects.filter(nombres__icontains=keyword)
    return JsonResponse([profesor.getJSONSimple() for profesor in profesores], safe=False)

@require_http_methods(["GET"])
def profesor(request):
    data_json = json.loads(request.body.decode('utf-8'))
    profesor_id = data_json['profesor_id']

    profesor = Profesor.objects.filter(id=profesor_id).first()
    if not profesor:
        return HttpResponseBadRequest("profesor inexistente")
    
    return JsonResponse(profesor.getAsesorias(), safe=False)

def seeders(request):
    n1 = Nivel(numero=8)
    n1.save()
    c1 = Carrera(nombre="Ingenieria de sistemas")
    c1.save()
    periodo1 = Periodo(codigo=20241)
    periodo1.save()
    
    curso1 = Curso(nombre="Ingenieria de Software 2", carrera=c1, nivel=n1)
    curso1.save()
    curso2 = Curso(nombre="Gestion de Riesgos", carrera=c1, nivel=n1)
    curso2.save()
    curso3 = Curso(nombre="Taller de propuesta de investigacion", carrera=c1, nivel=n1)
    curso3.save()

    p1 = Profesor(nombres="Hernan Nina", foto="a")
    p1.save()
    p2 = Profesor(nombres="Nehil Muñoz", foto="b")
    p2.save()
    p3 = Profesor(nombres="Copernico", foto="c")
    p3.save()
    p4 = Profesor(nombres="Pablito", foto="d")
    p4.save()

    a1 = Asesoria(fecha_inicio=datetime(2024, 5, 1, 12, 00), fecha_fin=datetime(2024, 5, 1, 13, 00), enlace="enlace1", ambiente="O1")
    a1.save()
    a2 = Asesoria(fecha_inicio=datetime(2024, 5, 2, 10, 00), fecha_fin=datetime(2024, 5, 2, 11, 00), enlace="enlace2", ambiente="O2")
    a2.save()
    a3 = Asesoria(fecha_inicio=datetime(2024, 5, 6, 11, 00), fecha_fin=datetime(2024, 5, 2, 12, 00), enlace=f"enlace3", ambiente=f"O1")
    a3.save()
    a4 = Asesoria(fecha_inicio=datetime(2024, 5, 6, 12, 00), fecha_fin=datetime(2024, 5, 2, 13, 00), enlace=f"enlace4", ambiente=f"O2")
    a4.save()
    a5 = Asesoria(fecha_inicio=datetime(2024, 5, 10, 10, 00), fecha_fin=datetime(2024, 5, 2, 10, 00), enlace=f"enlace5", ambiente=f"O1")
    a5.save()
    a6 = Asesoria(fecha_inicio=datetime(2024, 5, 11, 16, 00), fecha_fin=datetime(2024, 5, 2, 16, 00), enlace=f"enlace6", ambiente=f"O1")
    a6.save()
    a7 = Asesoria(fecha_inicio=datetime(2024, 5, 11, 18, 00), fecha_fin=datetime(2024, 5, 2, 19, 00), enlace=f"enlace7", ambiente=f"O2")
    a7.save()
    a8 = Asesoria(fecha_inicio=datetime(2024, 5, 1, 18, 00), fecha_fin=datetime(2024, 5, 2, 19, 00), enlace=f"enlace8", ambiente=f"O1")
    a8.save()

    seccion1_1 = Seccion(codigo=840, curso=curso1, periodo=periodo1, profesor=p1, asesoria=a1)
    seccion1_1.save()
    seccion1_2 = Seccion(codigo=841, curso=curso1, periodo=periodo1, profesor=p2, asesoria=a2)
    seccion1_2.save()
    seccion1_3 = Seccion(codigo=842, curso=curso1, periodo=periodo1, profesor=p3, asesoria=a3)
    seccion1_3.save()
    seccion2_1 = Seccion(codigo=2001, curso=curso2, periodo=periodo1, profesor=p1, asesoria=a4)
    seccion2_1.save()
    seccion2_2 = Seccion(codigo=2002, curso=curso2, periodo=periodo1, profesor=p1, asesoria=a5)
    seccion2_2.save()
    seccion3_1 = Seccion(codigo=3001, curso=curso3, periodo=periodo1, profesor=p2, asesoria=a6)
    seccion3_1.save()
    seccion3_2 = Seccion(codigo=3002, curso=curso3, periodo=periodo1, profesor=p1, asesoria=a7)
    seccion3_2.save()
    seccion3_3 = Seccion(codigo=3003, curso=curso3, periodo=periodo1, profesor=p4, asesoria=a8)
    seccion3_3.save()

    e1 = Estudiante(nombres="David", correo="david@gmail.com")
    e1.save()
    e2 = Estudiante(nombres="Piero", correo="piero@gmail.com")
    e2.save()
    e3 = Estudiante(nombres="Cliff", correo="cliff@gmail.com")
    e3.save()

    r1 = Reserva(codigo=123, estudiante=e1, asesoria=a1)
    r1.save()
    r2 = Reserva(codigo=456, estudiante=e1, asesoria=a2)
    r2.save()
    r3 = Reserva(codigo=456, estudiante=e1, asesoria=a4)
    r3.save()
    r4 = Reserva(codigo=456, estudiante=e2, asesoria=a1)
    r4.save()
    r5 = Reserva(codigo=456, estudiante=e2, asesoria=a2)
    r5.save()
    r6 = Reserva(codigo=456, estudiante=e2, asesoria=a3)
    r6.save()
    r7 = Reserva(codigo=456, estudiante=e2, asesoria=a4)
    r7.save()
    r8 = Reserva(codigo=456, estudiante=e2, asesoria=a7)
    r8.save()

    admin = Administrador(nombres="Admin", celular="999999999")
    admin.save()

    c1 = Cuenta(usuario="david123", contrasenha="123", persona=e1)
    c1.save()
    c2 = Cuenta(usuario="piero456", contrasenha="456", persona=e2)
    c2.save()
    c3 = Cuenta(usuario="cliff789", contrasenha="789", persona=e3)
    c3.save()
    c4 = Cuenta(usuario="admin", contrasenha="admin", persona=admin)
    c4.save()


    return JsonResponse({"mensaje":"completed"})



def test(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        username = data_json['username']
        password = data_json['password']
        names = data_json['names']
        email = data_json['email']
        cuenta = Cuenta.objects.filter(usuario=username).exists()
        if cuenta:
            tipo = 0
            mensaje = "Usuario ya existe"
        else:
            cuenta = Cuenta(usuario=username, contrasenha=password)
            cuenta.save()
            estudiante =  Estudiante(nombres=names, correo=email, cuenta=cuenta)
            registro = RegistroPersonas.get_instance()
            registro.agregar(estudiante)
            print("----")
            registro.imprimir()
            print("----")
            registro.save()
            return JsonResponse({"message":"bien"})
    return JsonResponse({"message":"error"})
