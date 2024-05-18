Django tutorial:
https://www.w3schools.com/django/django_views.php

Pasos:
1. Iniciar el venv (myworld\Scripts\activate.bat)
2. Moverse al proyecto (cd sw2back)
3. Ejecutar el proyecto (py manage.py runserver)

Modelos y Clases en Django:
https://docs.djangoproject.com/en/5.0/topics/db/models/

## Testear APIs

| Acción                       | Comando curl                                                                                                                                                     | Contenido JSON                                                                 |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| **Registrar Usuario**          | `curl -X POST http://127.0.0.1:8000/registrar/ -H 'Content-Type: application/json' -d @pruebita.json`                                                             | `{ "usuario": "test", "contrasenha": "test", "nombres": "Test", "correo": "test@gmail.com" }`       |
| **Iniciar Sesión**             | `curl -X POST http://127.0.0.1:8000/login/ -H 'Content-Type: application/json' -d @pruebita.json`                                                                 | `{ "usuario": "test", "contrasenha": "test" }`                                                             |
| **Obtener Asesorías de Estudiante** | `curl -X POST http://127.0.0.1:8000/asesorias_estudiante/ -H 'Content-Type: application/json' -d @pruebita.json`                                                 | `{ "estudiante_id": "144" }`                                                                                       |
| **Buscar Profesores**          | `curl -X POST http://127.0.0.1:8000/profesores/ -H 'Content-Type: application/json' -d @pruebita.json`                                                            | `{ "keyword": "nin" }`                                                                                             |
| **Obtener Detalles de un Profesor** | `curl -X POST http://127.0.0.1:8000/profesor/ -H 'Content-Type: application/json' -d @pruebita.json`                                                            | `{ "profesor_id": "24" }`                                                                                           |
| **Reservar Asesoría**          | `curl -X POST http://127.0.0.1:8000/reservar/ -H 'Content-Type: application/json' -d @pruebita.json`                                                              | `{ "estudiante_id": "144", "asesoria_id": "15" }`                                                                   |
| **Cargar Datos de Excel**      | `curl -X POST -F "excel_secciones=@2024-1_Horarios_Cursos_Sección.xlsx" -F "excel_asesorias=@Atención_alumnos_2024-1.xlsx" -d '{"periodo": "2024-1", "fecha_inicio": "2024-04-01"}' http://127.0.0.1:8000/cargar/` | `{ "periodo": "2024-1", "fecha_inicio": "2024-04-01" }`                                                             |

## Usar APIs

| Acción                                | Método | URL                                         | JSON a enviar                                                                                          | JSON a recibir |
|---------------------------------------|--------|---------------------------------------------|----------------------------------------------------------------------------------------------------------|----------------|
| **Registrar Usuario**                 | POST   | http://127.0.0.1:8000/registrar/            | `{ "usuario": "test", "contrasenha": "test", "nombres": "Test", "correo": "test@gmail.com" }`            | [Ver JSON](#json-a-recibir-de-registrar) |
| **Iniciar Sesión**                    | POST   | http://127.0.0.1:8000/login/                | `{ "usuario": "test", "contrasenha": "test" }`                                                          | [Ver JSON](#json-a-recibir-de-login) |
| **Obtener Asesorías de Estudiante**   | POST   | http://127.0.0.1:8000/asesorias_estudiante/ | `{ "estudiante_id": "143" }`                                                                             | [Ver JSON](#json-a-recibir-de-asesorias_estudiante) |
| **Buscar Profesores**                 | POST   | http://127.0.0.1:8000/profesores/           | `{ "keyword": "nin" }`                                                                                   | [Ver JSON](#json-a-recibir-de-profesores) |
| **Obtener Detalles de un Profesor**   | POST   | http://127.0.0.1:8000/profesor/             | `{ "profesor_id": "24" }`                                                                                 | [Ver JSON](#json-a-recibir-de-profesor) |
| **Reservar Asesoría**                 | POST   | http://127.0.0.1:8000/reservar/             | `{ "estudiante_id": "144", "asesoria_id": "15" }`                                                         | [Ver JSON](#json-a-recibir-de-reservar) |
| **Cargar Datos de Excel**             | POST   | http://127.0.0.1:8000/cargar/               | `-F "excel_secciones=@2024-1_Horarios_Cursos_Sección.xlsx" -F "excel_asesorias=@Atención_alumnos_2024-1.xlsx" -d '{"periodo": "2024-1", "fecha_inicio": "2024-04-01"}'` | [Ver JSON](#json-a-recibir-de-cargar) |


## Ejemplos de lo que el front recibe del back

#### JSON a recibir de ```registrar/```
```json
{
  "id": 2,
  "usuario": "test",
  "contrasenha": "test",
  "persona": {
    "id": 144,
    "tipo": "Estudiante",
    "nombres": "Test",
    "correo": "test@gmail.com"
  }
}
```

#### JSON a recibir de ```login/```
```json
{
  "id": 2,
  "usuario": "test",
  "contrasenha": "test",
  "persona": {
    "id": 144,
    "tipo": "Estudiante",
    "nombres": "Test",
    "correo": "test@gmail.com"
  }
}
```

#### JSON a recibir de ```asesorias_estudiante/```
```json
[
  {
    "id": 3,
    "codigo": 1716043281,
    "asesoria": {
      "id": 15,
      "fecha_inicio": "2024-07-12T14:00:00Z",
      "fecha_fin": "2024-07-12T15:00:00Z",
      "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
      "ambiente": "Pab O2 - Piso 8 (1)",
      "seccion": {
        "id": 45,
        "codigo": 321,
        "curso": {
          "id": 3,
          "codigo": 5686,
          "nombre": "FUNDAMENTOS DE INGENIERÍA DE SISTEMAS",
          "carrera": {
            "id": 1,
            "nombre": "Ingenieria de sistemas"
          },
          "nivel": {
            "id": 1,
            "numero": 3
          }
        },
        "periodo": {
          "id": 1,
          "codigo": "2024-1"
        },
        "profesor": {
          "id": 24,
          "nombres": "CHECA FERNANDEZ, ROCIO DEL PILAR",
          "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4zzqg08h2mqFtrogllGFi42pI84d2mtpMMilSAFbsTwdioKIIaZ2d_U9IKsc&s"
        }
      }
    }
  },
  {
    "id": 4,
    "codigo": 1716043495,
    "asesoria": {
      "id": 16,
      "fecha_inicio": "2024-07-19T14:00:00Z",
      "fecha_fin": "2024-07-19T15:00:00Z",
      "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
      "ambiente": "Pab O2 - Piso 8 (1)",
      "seccion": {
        "id": 45,
        "codigo": 321,
        "curso": {
          "id": 3,
          "codigo": 5686,
          "nombre": "FUNDAMENTOS DE INGENIERÍA DE SISTEMAS",
          "carrera": {
            "id": 1,
            "nombre": "Ingenieria de sistemas"
          },
          "nivel": {
            "id": 1,
            "numero": 3
          }
        },
        "periodo": {
          "id": 1,
          "codigo": "2024-1"
        },
        "profesor": {
          "id": 24,
          "nombres": "CHECA FERNANDEZ, ROCIO DEL PILAR",
          "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4zzqg08h2mqFtrogllGFi42pI84d2mtpMMilSAFbsTwdioKIIaZ2d_U9IKsc&s"
        }
      }
    }
  }
]
```

#### JSON a recibir de ```profesores/```
```json
[
  {
    "id": 54,
    "nombres": "BIBOLOTTI SABLA, GIANNINA FARIDE",
    "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUEA49QjnIBhPCtvRShigtXYCt_oWr_-epxMeEH8LuS1lOqFzAHfld_yXkveU&s"
  },
  {
    "id": 72,
    "nombres": "NINA HANCO, HERNAN",
    "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqjMPo0KcUmC17J1VylyopnM8KWgKErvJkXmDEBv_yMgrJqh6BhO-l3tAgAg&s"
  },
  {
    "id": 76,
    "nombres": "QUIROZ VILLALOBOS, LENNIN PAUL",
    "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTL2ANIFcSgRxPC5eeuAYGWcg5Had0Lo10ZEEj7FdYy8HIPtPPb2IQu_450w&s"
  }
]
```

#### JSON a recibir de ```profesor/```
```json
{
  "id": 24,
  "nombres": "CHECA FERNANDEZ, ROCIO DEL PILAR",
  "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4zzqg08h2mqFtrogllGFi42pI84d2mtpMMilSAFbsTwdioKIIaZ2d_U9IKsc&s",
  "secciones": [
    {
      "id": 45,
      "codigo": 321,
      "curso": {
        "id": 3,
        "codigo": 5686,
        "nombre": "FUNDAMENTOS DE INGENIERÍA DE SISTEMAS",
        "carrera": {
          "id": 1,
          "nombre": "Ingenieria de sistemas"
        },
        "nivel": {
          "id": 1,
          "numero": 3
        }
      },
      "periodo": {
        "id": 1,
        "codigo": "2024-1"
      },
      "asesorias": [
        {
          "id": 8,
          "fecha_inicio": "2024-05-24T14:00:00Z",
          "fecha_fin": "2024-05-24T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        },
        {
          "id": 9,
          "fecha_inicio": "2024-05-31T14:00:00Z",
          "fecha_fin": "2024-05-31T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        },
        {
          "id": 10,
          "fecha_inicio": "2024-06-07T14:00:00Z",
          "fecha_fin": "2024-06-07T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        },
        {
          "id": 11,
          "fecha_inicio": "2024-06-14T14:00:00Z",
          "fecha_fin": "2024-06-14T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        },
        {
          "id": 12,
          "fecha_inicio": "2024-06-21T14:00:00Z",
          "fecha_fin": "2024-06-21T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        },
        {
          "id": 13,
          "fecha_inicio": "2024-06-28T14:00:00Z",
          "fecha_fin": "2024-06-28T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        },
        {
          "id": 14,
          "fecha_inicio": "2024-07-05T14:00:00Z",
          "fecha_fin": "2024-07-05T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        },
        {
          "id": 15,
          "fecha_inicio": "2024-07-12T14:00:00Z",
          "fecha_fin": "2024-07-12T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        },
        {
          "id": 16,
          "fecha_inicio": "2024-07-19T14:00:00Z",
          "fecha_fin": "2024-07-19T15:00:00Z",
          "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
          "ambiente": "Pab O2 - Piso 8 (1)"
        }
      ]
    },
    {
      "id": 51,
      "codigo": 321,
      "curso": {
        "id": 4,
        "codigo": 650001,
        "nombre": "INFORMÁTICA PARA LA GESTIÓN",
        "carrera": {
          "id": 1,
          "nombre": "Ingenieria de sistemas"
        },
        "nivel": {
          "id": 1,
          "numero": 3
        }
      },
      "periodo": {
        "id": 1,
        "codigo": "2024-1"
      },
      "asesorias": []
    },
    {
      "id": 220,
      "codigo": 728,
      "curso": {
        "id": 35,
        "codigo": 650021,
        "nombre": "INGENIERÍA DE SOFTWARE I",
        "carrera": {
          "id": 1,
          "nombre": "Ingenieria de sistemas"
        },
        "nivel": {
          "id": 5,
          "numero": 7
        }
      },
      "periodo": {
        "id": 1,
        "codigo": "2024-1"
      },
      "asesorias": []
    }
  ]
}
```

#### JSON a recibir de ```reservar/```
```json
{
  "id": 3,
  "codigo": 1716043281,
  "estudiante": {
    "id": 144,
    "tipo": "Estudiante",
    "nombres": "Test",
    "correo": "test@gmail.com"
  },
  "asesoria": {
    "id": 15,
    "fecha_inicio": "2024-07-12T14:00:00Z",
    "fecha_fin": "2024-07-12T15:00:00Z",
    "enlace": "https://ulima-edu-pe.zoom.us/j/5755344343?pwd=SXc2Q05JSEx1SFB4RWE4cWlZVkZWQT09",
    "ambiente": "Pab O2 - Piso 8 (1)"
  }
}
```

#### JSON a recibir de ```cargar/```
```json
{
  "data": "un json muy largo con la data de todos los cursos"
}
```
