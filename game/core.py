import re

from game.Arca import Arca
from game.Tripulante import Tripulante
from texts.texts import HELP_TEXT, TRIPULANTES_TEXT, SALAS_TEXT, LEYES_TEXT, NORMAS_TEXT
from typing import Optional

class User_state:
    id: int
    avatar: Optional[Tripulante]

    def __init__(self, id: int):
        self.id = id

class Bot_state:
    id: str
    arca: Arca
    users: list[User_state] = []

    def __init__(self, bot_id, arca):
        self.id = bot_id
        self.arca = arca

    def user(self, id: int):
        for user in self.users:
            if user.id == id:
                return user

        new_user = User_state(id)
        self.users.append(new_user)
        return new_user

def help():
    return HELP_TEXT

def run(state: Bot_state, user: User_state, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:
        case 'autodestrucción' | 'autodestruccion':
            if state.arca.health.is_arca_autodestructing == False:
                state.arca.health.is_arca_autodestructing = True
                return 'Autodestrucción programada para dentro de 30 minutos'
            else:
                return 'Autodestrucción ya había sido iniciada'

        case 'abortar':
            if state.arca.health.is_arca_autodestructing:
                state.arca.health.is_arca_autodestructing = False
                return 'Autodestrucción abortada'
            else:
                return 'No existe una secuencia de autodestrucción inicializada.'

        case 'consumir':
            state.arca.stocks["algasugos"].amount = state.arca.stocks["algasugos"].amount - 1
            return 'Se han consumido 1 algasugo'

    return f"El comando <{command}> no está implementado en la interfaz AURA"


def say(state: Bot_state, user: User_state, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:

        case 'tripulación' | 'tripulantes':
            return TRIPULANTES_TEXT

        case 'salas' | 'dependencias' | 'aforo':
            return SALAS_TEXT

        case 'leyes' | 'LGJ6' :
            return LEYES_TEXT

        case 'normas' | 'normativa' | 'reglas' | 'reglamento' :
            return NORMAS_TEXT

        case 'estado':
            return f"""
                ESTADO DEL ARCA\n
                - Bodega {state.arca.health.cellar}%\n
                - Reactor {state.arca.health.reactor}%\n
                - Exterior {state.arca.health.exterior}%\n
                - Sistema eléctrico {state.arca.health.circuits}%\n
                - Caldera {state.arca.health.boiler}%\n
                - Huertos {state.arca.health.gardens}%\n
                - Cabinas tripulantes {state.arca.health.sleeping_quarters}%
            """

        case 'inventario':
            inventario = "INVENTARIO DE SUMINISTROS"
            for stock in state.arca.stocks:
                cantidad = state.arca.stocks[stock].amount
                unidad = state.arca.stocks[stock].unit
                inventario += f"\n{stock.capitalize()} {cantidad}{unidad}"
            return inventario

        case 'combustible':
            return f"Combustible restante: {0} unidades"

        case _:
            return f"No existe información registrada para la propiedad: {command}."
