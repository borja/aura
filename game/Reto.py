from typing import Optional
import random

from game.Arca import Sala
from game.Tripulante import Atributos

class Obstaculo:
    tipo: str = "ciencia"
    requerimiento: int = 1
    dificultad: int = 5

    def __init__(self, tipo: str, requisito: int, dificultad: int):
        self.tipo = tipo
        self.requisito = requisito
        self.dificultad = dificultad

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        obs = Obstaculo('ciencia', 1, 5)
        obs.tipo = fuente.get('tipo', 'ciencia')
        obs.requerimiento = fuente.get('requerimiento', 1)
        obs.dificultad = fuente.get('dificultad', 5)
        return obs

    def to_dict(self):
        return {
            'tipo': self.tipo,
            'requerimiento': self.requerimiento,
            'dificultad': self.dificultad,
        }

    def es_capaz(self, atr: Atributos):
        nivel = _obtener_valor(self.tipo, atr)
        return nivel >= self.requerimiento

    def intentar(self, atr: Atributos):
        nivel = _obtener_valor(self.tipo, atr)
        exitos = 0
        for _ in range(nivel):
            diceResult = random.randrange(1, 10, 1)
            if diceResult >= self.dificultad:
                exitos += 1

        return exitos

def _obtener_valor(propiedad: str, atr: Atributos):
    match propiedad:
        case 'ciencia':
            return atr.ciencia
        case 'combate':
            return atr.combate
        case 'constitucion':
            return atr.constitucion
        case 'credibilidad':
            return atr.credibilidad
        case 'mecanica':
            return atr.mecanica
        case 'programacion':
            return atr.programacion


class Reto:
    id: str = ''
    nombre: str = ''
    descripcion: str = ''
    sala: Optional[Sala] = None
    activo: bool = True
    componentes: list[Obstaculo] = []

    @staticmethod
    def from_dict(fuente: dict[str, any], salas: list[Sala]):
        reto = Reto()
        reto.id = fuente.get('id', '')
        reto.nombre = fuente.get('nombre', '')
        reto.descripcion = fuente.get('descripcion', '')

        obstaculos_dict = fuente.get('componentes', [])
        reto.componentes = list(map((lambda obs_dict: Obstaculo.from_dict(obs_dict)), obstaculos_dict))

        reto.activo = fuente.get('activo', True)

        sala_id = fuente.get('sala', '')
        if sala_id != '':
            reto.sala = next((sala for sala in salas if sala.id == sala_id), None)

    def to_dict(self):
        obs = list(map((lambda obs: obs.to_dict()), self.componentes))
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'sala': '' if self.sala == None else self.sala.id,
            'activo': self.activo,
            'componentes': obs,
        }
    
    def es_capaz(self, atr: Atributos):
        for obstaculo in self.componentes:
            if obstaculo.es_capaz(atr) == False:
                return False
        return True
    
    def intentar(self, atr: Atributos):
        exitos = list(map(lambda obstaculo: obstaculo.intentar(atr), self.componentes))
        return min(exitos)





