from typing import Optional

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
        match self.tipo:
            case 'ciencia':
                return atr.ciencia >= self.requerimiento
            case 'combate':
                return atr.combate >= self.requerimiento
            case 'constitucion':
                return atr.constitucion >= self.requerimiento
            case 'credibilidad':
                return atr.credibilidad >= self.requerimiento
            case 'mecanica':
                return atr.mecanica >= self.requerimiento
            case 'programacion':
                return atr.programacion >= self.requerimiento


class Reto:
    id: str = ''
    name: str = ''
    description: str = ''
    sala: Optional[Sala] = None
    componentes: list[Obstaculo] = []

    @staticmethod
    def from_dict(fuente: dict[str, any], salas: list[Sala]):
        reto = Reto()
        reto.id = fuente.get('id', '')
        reto.name = fuente.get('name', '')
        reto.description = fuente.get('description', '')

        obstaculos_dict = fuente.get('componentes', [])
        reto.componentes = list(map((lambda obs_dict: Obstaculo.from_dict(obs_dict)), obstaculos_dict))

        sala_id = fuente.get('sala', '')
        if sala_id != '':
            reto.sala = next((sala for sala in salas if sala.id == sala_id), None)

    def to_dict(self):
        obs = list(map((lambda obs: obs.to_dict()), self.componentes))
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sala': '' if self.sala == None else self.sala.id,
            'componentes': obs,
        }




