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
curl -X GET http://127.0.0.1:8000/profesor/ -H 'Content-Type: application/json' -d @pruebita.json