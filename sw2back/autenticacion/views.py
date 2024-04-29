from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize

from autenticacion.models import *

# Create your views here.
def register(request):
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
            estudiante.save()
            tipo = estudiante.getTipo()
            mensaje = "Cuenta creada correctamente"

    return JsonResponse({
        "type":tipo,
        "message": mensaje
    })

def login(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        username = data_json['username']
        password = data_json['password']
        cuenta = Cuenta.objects.filter(usuario=username, contrasenha=password).exists()
        if cuenta:
            cuenta = Cuenta.objects.filter(usuario=username, contrasenha=password).first()
            es_estudiante = Estudiante.objects.filter(cuenta=cuenta).exists()
            es_administrador = Administrador.objects.filter(cuenta=cuenta).exists()
            if es_estudiante:
                estudiante = Estudiante.objects.filter(cuenta=cuenta).first()
                return JsonResponse({
                    "type":estudiante.getTipo(),
                    "message": "Login exitoso",
                    "cuenta": cuenta.getJSON(),
                    "estudiante": estudiante.getJSON()
                })
            if es_administrador:
                administrador = Administrador.objects.filter(cuenta=cuenta).first()
                return JsonResponse({
                    "type":estudiante.getTipo(),
                    "message": "Login exitoso",
                    "cuenta": cuenta.getJSON(),
                    "administrador": administrador.getJSON()
                })
    return JsonResponse({
        "type": 0,
        "message": "Error"
    })