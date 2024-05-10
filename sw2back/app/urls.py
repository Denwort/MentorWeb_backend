from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('asesorias_estudiante/', views.asesorias_estudiante, name='asesorias_estudiante'),
    path('profesores/', views.profesores, name='profesores'),
    path('profesor/', views.profesor, name='profesor'),
    path('reservar/', views.reservar, name='reservar'),
    path('test/', views.test, name='test'),
    path('seeders/', views.seeders, name='seeders'),
]
