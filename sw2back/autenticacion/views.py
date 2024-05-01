from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
from autenticacion.models import *
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
        tipo = 0
        mensaje = "Usuario ya existe"
    else:
        estudiante =  Estudiante(nombres=names, correo=email)
        estudiante.save()
        cuenta = Cuenta(usuario=username, contrasenha=password, persona=estudiante)
        cuenta.save()
        tipo = estudiante.getTipo()
        mensaje = "Cuenta creada correctamente"
    return JsonResponse({
        "tipo": tipo,
        "mensaje": mensaje
    })

@require_http_methods(["POST"])
def login(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    username = data_json['usuario']
    password = data_json['contrasenha']
    cuenta = Cuenta.objects.filter(usuario=username, contrasenha=password).exists()
    if cuenta:
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
    return JsonResponse({
        "tipo": 0,
        "mensaje": "Cuenta no existente"
    })

@require_http_methods(["GET"])
def asesorias_estudiante(request):
    data_json = json.loads(request.body.decode('utf-8'))
    estudiante_id = data_json['estudiante_id']
    estudiante = Estudiante.objects.filter(id=estudiante_id).first()
    reservas = estudiante.reservas.all()

    informacion_asesorias = []
    for reserva in reservas:
        asesoria = reserva.asesoria
        profesor = asesoria.profesor
        seccion = asesoria.seccion
        periodo = seccion.periodo
        curso = seccion.curso
        carrera = curso.carrera
        nivel = curso.nivel
        informacion_asesoria = {
            'asesoria': {
                'codigo': reserva.codigo,
                'fecha_inicio': asesoria.fecha_inicio,
                'fecha_fin': asesoria.fecha_fin,
                'enlace': asesoria.enlace,
            },
            'seccion': {
                'codigo': seccion.codigo,
                'curso': curso.nombre,
                'periodo': periodo.codigo,
                'carrera': carrera.nombre,
                'nivel': nivel.numero
            },
            'profesor': {
                'nombre': profesor.nombres,
                'foto': profesor.foto
            }
        }
        informacion_asesorias.append(informacion_asesoria)
    return JsonResponse(informacion_asesorias, safe=False)

@require_http_methods(["GET"])
def profesores(request):
    data_json = json.loads(request.body.decode('utf-8'))
    keyword = data_json['keyword']
    profesores = Profesor.objects.filter(nombres__icontains=keyword)

    profesores_encontrados = []
    for profesor in profesores:
        profesor_info = {
            'id': profesor.id,
            'nombre': profesor.nombres,
            'foto': profesor.foto
        }
        profesores_encontrados.append(profesor_info)
    return JsonResponse(profesores_encontrados, safe=False)

@require_http_methods(["GET"])
def profesor(request):
    data_json = json.loads(request.body.decode('utf-8'))
    profesor_id = data_json['profesor_id']
    profesor = Profesor.objects.filter(id=profesor_id).first()
    asesorias = profesor.asesorias.all()
    lista_cursos = []
    lista_asesorias = []
    for asesoria in asesorias:
        seccion = asesoria.seccion
        periodo = seccion.periodo
        curso = seccion.curso
        nivel = curso.nivel
        carrera = curso.carrera

        lista_cursos.append(curso.getJSON())

        lista_asesorias.append({
            "id": asesoria.id,
            "fecha_inicio": asesoria.fecha_inicio,
            "fecha_fin": asesoria.fecha_fin,
            "curso": curso.nombre
        })

    return JsonResponse({
        "profesor": profesor.getJSON(),
        "cursos" : lista_cursos,
        "asesorias": lista_asesorias
    }, safe=False)

def seeders(request):
    n1 = Nivel(numero=8).save()
    c1 = Carrera(nombre="Ingenieria de sistemas").save()
    periodo1 = Periodo(codigo=20241).save()
    
    curso1 = Curso(nombre="Ingenieria de Software 2", nivel=n1, carrera=c1).save()
    curso2 = Carrera(nombre="Gestion de Riesgos", nivel=n1, carrera=c1).save()
    curso3 = Carrera(nombre="Taller de propuesta de investigacion", nivel=n1, carrera=c1).save()
    
    seccion1_1 = Seccion(codigo=840, curso=curso1, periodo=periodo1).save()
    seccion1_2 = Seccion(codigo=841, curso=curso1, periodo=periodo1).save()
    seccion1_3 = Seccion(codigo=842, curso=curso1, periodo=periodo1).save()
    seccion2_1 = Seccion(codigo=2001, curso=curso2, periodo=periodo1).save()
    seccion2_2 = Seccion(codigo=2002, curso=curso2, periodo=periodo1).save()
    seccion3_1 = Seccion(codigo=3001, curso=curso3, periodo=periodo1).save()
    seccion3_2 = Seccion(codigo=3002, curso=curso3, periodo=periodo1).save()
    seccion3_3 = Seccion(codigo=3003, curso=curso3, periodo=periodo1).save()

    p1 = Profesor(nombres="Hernan Nina", foto="a").save()
    p2 = Profesor(nombres="Nehil Muñoz", foto="b").save()
    p3 = Profesor(nombres="Copernico", foto="c").save()
    p4 = Profesor(nombres="Pablito", foto="d").save()
    a1 = Asesoria(fecha_inicio=datetime(2024, 5, 1, 12, 00), fecha_fin=datetime(2024, 5, 1, 13, 00), enlace="enlace1", ambiente="O1", profesor=p1, seccion=seccion1_1).save()
    a2 = Asesoria(fecha_inicio=datetime(2024, 5, 2, 10, 00), fecha_fin=datetime(2024, 5, 2, 11, 00), enlace="enlace2", ambiente="O2", profesor=p2, seccion=seccion1_2).save()
    a3 = Asesoria(fecha_inicio=datetime(2024, 5, 6, 11, 00), fecha_fin=datetime(2024, 5, 2, 12, 00), enlace=f"enlace3", ambiente=f"O1", profesor=p3, seccion=seccion1_3).save()
    a4 = Asesoria(fecha_inicio=datetime(2024, 5, 6, 12, 00), fecha_fin=datetime(2024, 5, 2, 13, 00), enlace=f"enlace4", ambiente=f"O2", profesor=p4, seccion=seccion2_1).save()
    a5 = Asesoria(fecha_inicio=datetime(2024, 5, 10, 10, 00), fecha_fin=datetime(2024, 5, 2, 10, 00), enlace=f"enlace5", ambiente=f"O1", profesor=p1, seccion=seccion2_2).save()
    a6 = Asesoria(fecha_inicio=datetime(2024, 5, 11, 16, 00), fecha_fin=datetime(2024, 5, 2, 16, 00), enlace=f"enlace6", ambiente=f"O1", profesor=p1, seccion=seccion3_1).save()
    a7 = Asesoria(fecha_inicio=datetime(2024, 5, 11, 18, 00), fecha_fin=datetime(2024, 5, 2, 19, 00), enlace=f"enlace7", ambiente=f"O2", profesor=p3, seccion=seccion3_2).save()
    a8 = Asesoria(fecha_inicio=datetime(2024, 5, 1, 18, 00), fecha_fin=datetime(2024, 5, 2, 19, 00), enlace=f"enlace8", ambiente=f"O1", profesor=p4, seccion=seccion3_3).save()

    e1 = Estudiante(nombres="David", correo="david@gmail.com").save()
    e2 = Estudiante(nombres="Piero", correo="piero@gmail.com").save()
    e3 = Estudiante(nombres="Carlos", correo="carlos@gmail.com").save()

    r1 = Reserva(codigo=123, estudiante=e1, asesoria=a1).save()
    r2 = Reserva(codigo=456, estudiante=e1, asesoria=a2).save()
    r3 = Reserva(codigo=456, estudiante=e1, asesoria=a4).save()
    r4 = Reserva(codigo=456, estudiante=e2, asesoria=a1).save()
    r5 = Reserva(codigo=456, estudiante=e2, asesoria=a2).save()
    r6 = Reserva(codigo=456, estudiante=e2, asesoria=a3).save()
    r7 = Reserva(codigo=456, estudiante=e2, asesoria=a4).save()
    r8 = Reserva(codigo=456, estudiante=e2, asesoria=a7).save()

    admin = Administrador(nombres="Admin", celular="999999999").save()

    c1 = Cuenta(usuario="david123", contrasenha="123", persona=e1).save()
    c1 = Cuenta(usuario="piero456", contrasenha="456", persona=e2).save()
    c1 = Cuenta(usuario="admin", contrasenha="admin", persona=e1).save()

    return JsonResponse({"mensaje":"completed"})


'''
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
'''