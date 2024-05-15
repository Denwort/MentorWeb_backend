from __future__ import annotations
from app.models import *
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
import json

# Patron Strategy
class Buscador():
    def __init__(self, strategy: Strategy):
        self._strategy = strategy
    @property
    def strategy(self) -> Strategy:
        return self._strategy
    @strategy.setter
    def strategy(self, strategy: Strategy):
        self._strategy = strategy

    def buscar(self, value):
        result = self._strategy.do_algorithm(value)
        return result

class Strategy(ABC):
    @abstractmethod
    def do_algorithm(self, id: int):
        pass

class StrategyCuenta(Strategy):
    def do_algorithm(self, user: int):
        return Cuenta.objects.get(usuario=user)

class StrategyEstudiante(Strategy):
    def do_algorithm(self, id: int):
        return Estudiante.objects.get(id=id)

class StrategyProfesor(Strategy):
    def do_algorithm(self, id: int):
        return Profesor.objects.get(id=id)
    
class StrategyProfesores(Strategy):
    def do_algorithm(self, keyword: str):
        return Profesor.objects.filter(nombres__icontains=keyword)

class StrategyAsesoria(Strategy):
    def do_algorithm(self, id: int):
        return Asesoria.objects.get(id=id)
    

# Patron Decorator

class Extractor():
    lista = []
    def extract(self):
        pass

class RequestExtractor(Extractor):
    def __init__(self, request):
        self.lista.clear()
        self.request = request
    def extract(self):
        data_json = json.loads(self.request.body.decode('utf-8'))
        res = []
        for l in self.lista:
            res.append(data_json[l])            
        return res

class Decorator(Extractor):
    _component: Extractor = None

    def __init__(self, component: Extractor):
        self._component = component

    @property
    def component(self) -> Extractor:
        return self._component

    def extract(self):
        return self._component.extract()

class DecoratorUsuario(Decorator):
    def extract(self):
        self.lista.append('usuario')
        return self.component.extract()
class DecoratorContrasenha(Decorator):
    def extract(self):
        self.lista.append('contrasenha')
        return self.component.extract()
class DecoratorNombres(Decorator):
    def extract(self):
        self.lista.append('nombres')
        return self.component.extract()
class DecoratorCorreo(Decorator):
    def extract(self):
        self.lista.append('correo')
        return self.component.extract()

class DecoratorEstudianteId(Decorator):
    def extract(self):
        self.lista.append('estudiante_id')
        return self.component.extract()
class DecoratorProfesorId(Decorator):
    def extract(self):
        self.lista.append('profesor_id')
        return self.component.extract()
class DecoratorKeyword(Decorator):
    def extract(self):
        self.lista.append('keyword')
        return self.component.extract()
class DecoratorAsesoriaId(Decorator):
    def extract(self):
        self.lista.append('asesoria_id')
        return self.component.extract()

    

    
# Singleton para marcar el Periodo actual y la fecha actual
# Lo utiliza Estudiante y Profesor para obtener: reservas en el periodo actual y secciones en el periodo actual
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    periodoActual = 20241
    def getPeriodoActual(self):
        return self.periodoActual
    def setPeriodoActual(self, nuevoPeriodo):
        self.periodoActual = nuevoPeriodo
    def getFechaActual(self):
        return datetime.now()

# Factory method para crear Cuentas y Personas


# Controlar el periodo actual

