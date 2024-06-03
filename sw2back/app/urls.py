from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.GestionCuentas.register, name='register'),
    path('login/', views.GestionCuentas.login, name='login'),
    
    path('asesorias_estudiante/', views.GestionPersonas.asesorias_estudiante, name='asesorias_estudiante'),
    path('profesores/', views.GestionPersonas.profesores, name='profesores'),
    path('profesor/', views.GestionPersonas.profesor, name='profesor'),

    path('reservar/', views.GestionAsesorias.reservar, name='reservar'),

    path('recientes/', views.GestionRepositorio.recientes, name='recientes'),
    path('cursos/', views.GestionRepositorio.cursos, name='cursos'),
    path('curso/', views.GestionRepositorio.curso, name='curso'),
    path('documentos/', views.GestionRepositorio.documentos, name='documentos'),
    path('documento/', views.GestionRepositorio.documento, name='documento'),

    path('buscar_seccion/', views.GestionTickets.buscar_seccion, name='buscar_seccion'),
    path('crear/', views.GestionTickets.crear, name='crear'),
    path('pendientes/', views.GestionTickets.pendientes, name='pendientes'),
    path('ticket/', views.GestionTickets.ticket, name='ticket'),
    path('aceptar/', views.GestionTickets.aceptar, name='aceptar'),
    path('rechazar/', views.GestionTickets.rechazar, name='rechazar'),
    path('tickets/', views.GestionTickets.tickets, name='tickets'),
    
    path('cargar/', views.GestionAdministrador.cargar, name='cargar'),
]
