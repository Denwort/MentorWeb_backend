from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.GestionCuentas.register, name='register'),
    path('login/', views.GestionCuentas.login, name='login'),
    path('recuperarPregunta/', views.GestionCuentas.recuperarPregunta, name='recuperarPregunta'),
    path('recuperarRespuesta/', views.GestionCuentas.recuperarRespuesta, name='recuperarRespuesta'),
    path('recuperarContrasenha/', views.GestionCuentas.recuperarContrasenha, name='recuperarContrasenha'),
    path('verPerfil/', views.GestionCuentas.verPerfil, name='verPerfil'),
    path('preguntasDeSeguridad/', views.GestionCuentas.preguntasDeSeguridad, name='preguntasDeSeguridad'),
    path('editarPerfilEstudiante/', views.GestionCuentas.editarPerfilEstudiante, name='editarPerfilEstudiante'),
    path('crear_cuenta_profesor/', views.GestionCuentas.crear_cuenta_profesor, name='crear_cuenta_profesor'),
    path('editarPerfilProfesor/', views.GestionCuentas.editarPerfilProfesor, name='editarPerfilProfesor'),
    
    path('asesorias_estudiante/', views.GestionAsesorias.asesorias_estudiante, name='asesorias_estudiante'),
    path('profesores/', views.GestionAsesorias.profesores, name='profesores'),
    path('profesor/', views.GestionAsesorias.profesor, name='profesor'),
    path('profesoresCursos/', views.GestionAsesorias.profesoresCursos, name='profesoresCursos'),
    path('reservar/', views.GestionAsesorias.reservar, name='reservar'),
    path('reservarEliminar/', views.GestionAsesorias.reservarEliminar, name='reservarEliminar'),
    path('abrir_extra/', views.GestionAsesorias.abrir_extra, name='abrir_extra'),
    path('cerrar_extra/', views.GestionAsesorias.cerrar_extra, name='cerrar_extra'),
    path('listar_extras/', views.GestionAsesorias.listar_extras, name='listar_extras'),
    path('profesor_listar_asesorias/', views.GestionAsesorias.profesor_listar_asesorias, name='profesor_listar_asesorias'),

    path('recientes/', views.GestionRepositorio.recientes, name='recientes'),
    path('cursos/', views.GestionRepositorio.cursos, name='cursos'),
    path('curso/', views.GestionRepositorio.curso, name='curso'),
    path('documentos/', views.GestionRepositorio.documentos, name='documentos'),
    path('documento/', views.GestionRepositorio.documento, name='documento'),

    path('buscar_seccion/', views.GestionTickets.buscar_seccion, name='buscar_seccion'),
    path('obtener_periodos/', views.GestionTickets.obtener_periodos, name='obtener_periodos'),
    path('obtener_cursos/', views.GestionTickets.obtener_cursos, name='obtener_cursos'),
    path('crear/', views.GestionTickets.crear, name='crear'),
    path('tickets_todos/', views.GestionTickets.tickets_todos, name='tickets_todos'),
    path('pendientes/', views.GestionTickets.pendientes, name='pendientes'),
    path('ticket/', views.GestionTickets.ticket, name='ticket'),
    path('aceptar/', views.GestionTickets.aceptar, name='aceptar'),
    path('rechazar/', views.GestionTickets.rechazar, name='rechazar'),
    path('tickets/', views.GestionTickets.tickets, name='tickets'),
    
    path('cargar/', views.GestionAdministrador.cargar, name='cargar'),
]
