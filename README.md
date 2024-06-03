Django tutorial:
https://www.w3schools.com/django/django_views.php

Pasos:
1. Iniciar el venv (myworld\Scripts\activate.bat)
2. Moverse al proyecto (cd sw2back)
3. Ejecutar el proyecto (py manage.py runserver)

Modelos y Clases en Django:
https://docs.djangoproject.com/en/5.0/topics/db/models/

## Apis

| Acción                                | URL                                         | JSON a enviar                                                                                          |
|---------------------------------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------|
| **Registrar Usuario**                 | http://127.0.0.1:8000/registrar/            | `{ "usuario": "test", "contrasenha": "test", "nombres": "Test", "correo": "test@gmail.com" }`            |
| **Iniciar Sesión**                    | http://127.0.0.1:8000/login/                | `{ "usuario": "test", "contrasenha": "test" }`                                                          |
| **Obtener Asesorías de Estudiante**   | http://127.0.0.1:8000/asesorias_estudiante/ | `{ "estudiante_id": "143" }`                                                                             |
| **Buscar Profesores**                 | http://127.0.0.1:8000/profesores/           | `{ "keyword": "nin" }`                                                                                   |
| **Obtener Detalles de un Profesor**   | http://127.0.0.1:8000/profesor/             | `{ "profesor_id": "24" }`                                                                                 |
| **Reservar Asesoría**                 | http://127.0.0.1:8000/reservar/             | `{ "estudiante_id": "144", "asesoria_id": "15" }`                                                         |
| **Cargar Datos de Excel**             | http://127.0.0.1:8000/cargar/               | `-F "excel_secciones=@2024-1_Horarios_Cursos_Sección.xlsx" -F "excel_asesorias=@Atención_alumnos_2024-1.xlsx" -d '{"periodo": "2024-1", "fecha_inicio": "2024-04-01"}'` |
| **Obtener Periodos**                  | http://127.0.0.1:8000/periodos/             | `{}`                                                                                                     |
| **Obtener Cursos**                    | http://127.0.0.1:8000/cursos/               | `{}`                                                                                                     |
| **Buscar Sección**                    | http://127.0.0.1:8000/buscar_seccion/       | `{ "periodo_id": "1", "curso_id": "2" }`                                                                 |
| **Crear Ticket**                      | http://127.0.0.1:8000/crear/                | `-F "estudiante_id=144" -F "seccion_id=101" -F "asunto=Asunto del ticket" -F "comentario=Comentario del ticket" -F "archivo=@ruta/al/archivo.pdf"` |
| **Obtener Tickets Pendientes**        | http://127.0.0.1:8000/pendientes/           | `{}`                                                                                                     |
| **Obtener Detalle de Ticket**         | http://127.0.0.1:8000/ticket/               | `{ "ticket_id": "1" }`                                                                                   |
| **Aceptar Ticket**                    | http://127.0.0.1:8000/aceptar/              | `{ "ticket_id": "1", "comentario": "Comentario de aceptación", "nombre": "Nombre del documento", "descripcion": "Descripción del documento" }` |
| **Rechazar Ticket**                   | http://127.0.0.1:8000/rechazar/             | `{ "ticket_id": "1", "comentario": "Comentario de rechazo" }`                                            |

**Nota:** Todos los endpoints utilizan el método POST.
