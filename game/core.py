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
            return f"El comando: '{command}' no está implementado en la interfaz AURA"

def print_estado(sth):
    return f"""
        *ESTADO DEL ARCA*\n
        {sth.cellar}% *Bodega*
        {sth.reactor}% *Reactor*
        {sth.exterior}% *Exterior*
        {sth.circuits}% *Sistema eléctrico*
        {sth.boiler}% *Caldera*
        {sth.gardens}% *Huertos*
        {sth.sleeping_quarters}% *Cabinas tripulantes*
    """

def say(state: Bot, user: User, command_text: str):
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
            return print_estado(state.arca.health)

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

def scan(state: Bot, user: Bot):
    print(colored(" ⚠️ WARNING: SCAN feature is not implemented",'orange'))
    return state.txts.txt_scan
