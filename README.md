Django tutorial:
https://www.w3schools.com/django/django_views.php

Pasos:
1. Crear el venv (py -m venv myworld) (pip install django) (pip install django-cors-headers)
1. Iniciar el venv (myworld\Scripts\activate.bat)
2. Moverse al proyecto (cd sw2back)
3. Ejecutar el proyecto (py manage.py runserver)

Modelos y Clases en Django:
https://docs.djangoproject.com/en/5.0/topics/db/models/

Testear APIs:
curl -X POST http://127.0.0.1:8000/login/ -H 'Content-Type: application/json' -d @pruebita.json

APIS

|Name                  |Metodo |Enviar                                    |Recibir |
|----------------------|-------|------------------------------------------|--------|
|http://127.0.0.1:8000/asesorias_estudiante/ |POST   |{"estudiante_id": "id del estudiante"}    |[aqui](#recibir-de-asesorias_estudiante) |
|http://127.0.0.1:8000/profesores/           |POST   |{"keyword": "texto para buscar al profe"} |[aqui](#recibir-de-profesores) |
|http://127.0.0.1:8000/profesor/             |POST   |{"profesor_id": "id del profesor"}        |[aqui](#recibir-de-profesor)   |
|http://127.0.0.1:8000/reservar/             |POST   |{"estudiante_id": "id del estudiante", "asesoria_id": "id de la asesoria"}        |[aqui](#recibir-de-reservar)   |

### Ejemplos de lo que el front recibe del back

#### Recibir de ```asesorias_estudiante/```

```json
[
  {
    "id": 1,
    "codigo": 123,
    "asesoria": {
      "id": 1,
      "fecha_inicio": "2024-05-01T12:00:00Z",
      "fecha_fin": "2024-05-01T13:00:00Z",
      "enlace": "enlace1",
      "ambiente": "O1",
      "seccion": {
        "id": 1,
        "codigo": 840,
        "curso": {
          "id": 1,
          "nombre": "Ingenieria de Software 2",
          "carrera": {
            "id": 1,
            "nombre": "Ingenieria de sistemas"
          },
          "nivel": {
            "id": 1,
            "numero": 8
          }
        },
        "periodo": {
          "id": 1,
          "codigo": 20241
        },
        "profesor": {
          "id": 1,
          "nombres": "Hernan Nina",
          "foto": "a"
        }
      }
    }
  },
  {
    "id": 2,
    "codigo": 456,
    "asesoria": {
      "id": 2,
      "fecha_inicio": "2024-05-02T10:00:00Z",
      "fecha_fin": "2024-05-02T11:00:00Z",
      "enlace": "enlace2",
      "ambiente": "O2",
      "seccion": {
        "id": 2,
        "codigo": 841,
        "curso": {
          "id": 1,
          "nombre": "Ingenieria de Software 2",
          "carrera": {
            "id": 1,
            "nombre": "Ingenieria de sistemas"
          },
          "nivel": {
            "id": 1,
            "numero": 8
          }
        },
        "periodo": {
          "id": 1,
          "codigo": 20241
        },
        "profesor": {
          "id": 2,
          "nombres": "Nehil Muñoz",
          "foto": "b"
        }
      }
    }
  },
  {
    "id": 3,
    "codigo": 456,
    "asesoria": {
      "id": 4,
      "fecha_inicio": "2024-05-06T12:00:00Z",
      "fecha_fin": "2024-05-02T13:00:00Z",
      "enlace": "enlace4",
      "ambiente": "O2",
      "seccion": {
        "id": 4,
        "codigo": 2001,
        "curso": {
          "id": 2,
          "nombre": "Gestion de Riesgos",
          "carrera": {
            "id": 1,
            "nombre": "Ingenieria de sistemas"
          },
          "nivel": {
            "id": 1,
            "numero": 8
          }
        },
        "periodo": {
          "id": 1,
          "codigo": 20241
        },
        "profesor": {
          "id": 1,
          "nombres": "Hernan Nina",
          "foto": "a"
        }
      }
    }
  }
]
```

#### Recibir de ```profesores/```

```json
[
  {
    "id": 1,
    "nombres": "Hernan Nina",
    "foto": "a"
  },
  {
    "id": 2,
    "nombres": "Nehil Muñoz",
    "foto": "b"
  },
  {
    "id": 3,
    "nombres": "Copernico",
    "foto": "c"
  }
]
```

#### Recibir de ```profesor/```

```json
{
  "id": 1,
  "nombres": "Hernan Nina",
  "foto": "a",
  "secciones": [
    {
      "id": 1,
      "codigo": 840,
      "curso": {
        "id": 1,
        "nombre": "Ingenieria de Software 2",
        "carrera": {
          "id": 1,
          "nombre": "Ingenieria de sistemas"
        },
        "nivel": {
          "id": 1,
          "numero": 8
        }
      },
      "periodo": {
        "id": 1,
        "codigo": 20241
      },
      "asesoria": {
        "id": 1,
        "fecha_inicio": "2024-05-01T12:00:00Z",
        "fecha_fin": "2024-05-01T13:00:00Z",
        "enlace": "enlace1",
        "ambiente": "O1"
      }
    },
    {
      "id": 4,
      "codigo": 2001,
      "curso": {
        "id": 2,
        "nombre": "Gestion de Riesgos",
        "carrera": {
          "id": 1,
          "nombre": "Ingenieria de sistemas"
        },
        "nivel": {
          "id": 1,
          "numero": 8
        }
      },
      "periodo": {
        "id": 1,
        "codigo": 20241
      },
      "asesoria": {
        "id": 4,
        "fecha_inicio": "2024-05-06T12:00:00Z",
        "fecha_fin": "2024-05-02T13:00:00Z",
        "enlace": "enlace4",
        "ambiente": "O2"
      }
    },
    {
      "id": 5,
      "codigo": 2002,
      "curso": {
        "id": 2,
        "nombre": "Gestion de Riesgos",
        "carrera": {
          "id": 1,
          "nombre": "Ingenieria de sistemas"
        },
        "nivel": {
          "id": 1,
          "numero": 8
        }
      },
      "periodo": {
        "id": 1,
        "codigo": 20241
      },
      "asesoria": {
        "id": 5,
        "fecha_inicio": "2024-05-10T10:00:00Z",
        "fecha_fin": "2024-05-02T10:00:00Z",
        "enlace": "enlace5",
        "ambiente": "O1"
      }
    },
    {
      "id": 7,
      "codigo": 3002,
      "curso": {
        "id": 3,
        "nombre": "Taller de propuesta de investigacion",
        "carrera": {
          "id": 1,
          "nombre": "Ingenieria de sistemas"
        },
        "nivel": {
          "id": 1,
          "numero": 8
        }
      },
      "periodo": {
        "id": 1,
        "codigo": 20241
      },
      "asesoria": {
        "id": 7,
        "fecha_inicio": "2024-05-11T18:00:00Z",
        "fecha_fin": "2024-05-02T19:00:00Z",
        "enlace": "enlace7",
        "ambiente": "O2"
      }
    }
  ]
}
```

#### Recibir de ```reservar/```

```json
{
  "id": 11,
  "codigo": 1715350463,
  "estudiante": {
    "id": 5,
    "nombres": "David",
    "correo": "david@gmail.com"
  },
  "asesoria": {
    "id": 2,
    "fecha_inicio": "2024-05-02T10:00:00Z",
    "fecha_fin": "2024-05-02T11:00:00Z",
    "enlace": "enlace2",
    "ambiente": "O2"
  }
}
```
