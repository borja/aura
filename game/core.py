import re

from typing import Optional
from termcolor import colored
from game.Arca import Arca
from game.Bot import Bot
from game.Tripulante import Tripulante
from game.User import User
from infra.Texts import Texts

def start(state: Bot, user: User):
    return state.txts.txt_welcome

def help(state: Bot, user: User):
    return state.txts.txt_ayuda

def run(state: Bot, user: User, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:
        case 'autodestrucción' | 'autodestruccion':
            if state.arca.health.is_arca_autodestructing is False:
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
            state.arca.stocks["algolosina"].amount = state.arca.stocks["algolosina"].amount - 1
            return 'Se han consumido 1 algolosina'

        case _:
            print(colored(f"⚠️ - Invalid command request: {command}",'yellow'))
            return f"El comando <{command}> no está implementado en la interfaz AURA"

def say(state: Bot, user: User, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:

        case 'tripulación' | 'tripulantes':
            return state.txts.txt_tripulantes

        case 'salas' | 'dependencias' | 'aforo':
            return state.txts.txt_salas

        case 'leyes' | 'LGJ6' :
            return state.txts.txt_leyes

        case 'normas' | 'normativa' | 'reglas' | 'reglamento' :
            return state.txts.txt_normas

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

def scan(state: Bot, user: User):
    return state.txts.txt_scan

