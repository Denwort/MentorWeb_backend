from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods

from autenticacion.models import *

# Create your views here.
@require_http_methods(["POST"])
def register(request):
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
        estudiante =  Estudiante(nombres=names, correo=email)
        estudiante.save()
        cuenta = Cuenta(usuario=username, contrasenha=password, persona=estudiante)
        cuenta.save()
        tipo = estudiante.getTipo()
        mensaje = "Cuenta creada correctamente"
    return JsonResponse({
        "type":tipo,
        "message": mensaje
    })

@require_http_methods(["POST"])
def login(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    username = data_json['username']
    password = data_json['password']
    cuenta = Cuenta.objects.filter(usuario=username, contrasenha=password).exists()
    if cuenta:
        cuenta = Cuenta.objects.filter(usuario=username, contrasenha=password).first()
        persona = cuenta.persona
        if hasattr(persona, 'estudiante'):
            estudiante = Estudiante.objects.filter(cuenta=cuenta).first()
            return JsonResponse({
                "type":estudiante.getTipo(),
                "message": "Login exitoso",
                "cuenta": cuenta.getJSON(),
                "estudiante": estudiante.getJSON()
            })
        if hasattr(persona, 'administrador'):
            administrador = Administrador.objects.filter(cuenta=cuenta).first()
            return JsonResponse({
                "type":estudiante.getTipo(),
                "message": "Login exitoso",
                "cuenta": cuenta.getJSON(),
                "administrador": administrador.getJSON()
            })
    return JsonResponse({
        "type": 0,
        "message": "Cuenta no existente"
    })

@require_http_methods(["GET"])
def asesorias_estudiante(request):
    data_json = json.loads(request.body.decode('utf-8'))
    estudiante_id = data_json['estudiante_id']
    estudiante = Estudiante.objects.filter(id=estudiante_id)
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

def seeders(request):
    p1 = Profesor(nombres="Pepe", foto="a")
    p2 = Profesor(nombres="Pedro", foto="b")
    p3 = Profesor(nombres="Copernico", foto="c")
    p4 = Profesor(nombres="Pablito", foto="d")
    p1.save()
    p2.save()
    p3.save()
    p4.save()
    return JsonResponse({"message":"completed"})