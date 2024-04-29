from abc import abstractmethod
from django.db import models
import json

# Create your models here.

class Cuenta(models.Model):
    usuario = models.CharField(max_length=255, unique=True)
    contrasenha = models.CharField(max_length=255)
    def __str__(self):
        return "Cuenta={usuario=" + self.usuario + "; contrasenha= " + self.contrasenha + "}"
    def getJSON(self):
        return {
            "usuario": self.usuario,
            "contrasenha": self.contrasenha
        }
    
class Persona(models.Model):
    class Meta:
        abstract: True
    nombres = models.CharField(max_length=255)
    cuenta = models.OneToOneField(
        Cuenta,
        on_delete=models.CASCADE,
        primary_key=True,
        blank=False
    )
    def __str__(self):
        pass
    @abstractmethod
    def getTipo(self):
        pass
    def getJSON(self):
        pass

class Estudiante(Persona):
    correo = models.CharField(max_length=255)
    def getTipo(self):
        return 1
    def __str__(self):
        return "Estudiante={nombres=" + self.nombres + "; correo=" + self.correo + "; cuenta=" + str(self.cuenta)
    def getJSON(self):
        return {
            "nombres": self.nombres,
            "correo": self.correo
        }

class Administrador(Persona):
    celular = models.CharField(max_length=255)
    def getTipo(self):
        return 3
    def __str__(self):
        return "Administrador={nombres=" + self.nombres + "; celular=" + self.celular + "; cuenta=" + str(self.cuenta)
    def getJSON(self):
        return {
            "nombres": self.nombres,
            "celular": self.celular
        }
