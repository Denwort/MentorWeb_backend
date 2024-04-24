from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def registrar(request):
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }
    return JsonResponse(data)