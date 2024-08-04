import re

from typing import Optional
from termcolor import colored
from game.Arca import Arca
from game.Tripulante import Tripulante
from infra.Texts import Texts

class User_state:
    id: int
    avatar: Optional[Tripulante]

    def __init__(self, id: int):
        self.id = id

class Bot_state:
    id: str
    txts: Texts
    arca: Arca
    users: list[User_state] = []

    def __init__(self, bot_id: str, arca: Arca, txts: Texts):
        self.id = bot_id
        self.arca = arca
        self.txts = txts

    def user(self, id: int):
        for user in self.users:
            if user.id == id:
                return user

        new_user = User_state(id)
        self.users.append(new_user)
        return new_user

def help(state: Bot_state, user: User_state):
    return state.txts.txt_ayuda

def run(state: Bot_state, user: User_state, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:
        case 'autodestrucción' | 'autodestruccion':
            if state.arca.health.is_arca_autodestructing is False:
                state.arca.health.is_arca_autodestructing = True
                print(colored(f" 🤖 {command} - Autodestrucción INICIADA",'green'))
                return 'Autodestrucción programada para dentro de 30 minutos'
            else:
                print(colored(f" 🤖 {command} - Ya había un proceso en curso",'yellow'))
                return 'Autodestrucción ya había sido iniciada'

        case 'abortar':
            if state.arca.health.is_arca_autodestructing:
                state.arca.health.is_arca_autodestructing = False
                print(colored(f" 🤖 {command} - Autodestrucción abortada",'green'))
                return 'Autodestrucción abortada'
            else:
                print(colored(f" 🤖 {command} - No existe secuencia de autodestrucción",'yellow'))
                return 'No existe una secuencia de autodestrucción inicializada.'

        case 'consumir':
            state.arca.stocks["algolosina"].amount -= 1
            print(colored(f" 🤖 {command} - 1 algolosina. Restantes: {state.arca.stocks["algolosina"].amount}",'green'))
            return 'Se han consumido 1 algolosina'

        case _:
            print(colored(f" ⚠️ - Invalid command request: {command}",'yellow'))
            return f"El comando \<{command}\> no está implementado en la interfaz AURA"

def say(state: Bot_state, user: User_state, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:

        case 'tripulación' | 'tripulantes':
            print(colored(f" 🤖 {command} - lista de tripulantes",'green'))
            return state.txts.txt_tripulantes

        case 'salas' | 'dependencias' | 'aforo':
            print(colored(f" 🤖 {command} - lista de salas",'green'))
            return state.txts.txt_salas

        case 'leyes' | 'LGJ6' :
            print(colored(f" 🤖 {command} - lista de Leyes",'green'))
            return state.txts.txt_leyes

        case 'normas' | 'normativa' | 'reglas' | 'reglamento' :
            print(colored(f" 🤖 {command} - lista de Reglas",'green'))
            return state.txts.txt_normas

        case 'estado':
            print(colored(f" 🤖 {command} - Estado del ARCA",'green'))
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
            print(colored(f" 🤖 {command} - Inventario",'green'))
            return inventario

        case 'combustible':
            combustible_restante = 0
            print(colored(f" 🤖 {command} - Restante: {combustible_restante}",'green'))
            return f"Combustible restante: {combustible_restante} unidades"

        case _:
            print(colored(f" ⚠️ - Invalid information request: {command}",'yellow'))
            return f"No existe información registrada para la propiedad: {command}"

def scan(state: Bot_state, user: User_state):
    return state.txts.txt_scan
