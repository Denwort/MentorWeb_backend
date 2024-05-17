from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.GestionCuentas.register, name='register'),
    path('login/', views.GestionCuentas.login, name='login'),
    path('asesorias_estudiante/', views.GestionPersonas.asesorias_estudiante, name='asesorias_estudiante'),
    path('profesores/', views.GestionPersonas.profesores, name='profesores'),
    path('profesor/', views.GestionPersonas.profesor, name='profesor'),
    path('reservar/', views.GestionAsesorias.reservar, name='reservar'),
    path('cargar/', views.GestionarAdministrador.cargar, name='cargar'),
]
