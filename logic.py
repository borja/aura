import re

from texts import HELP_TEXT, TRIPULANTES_TEXT, SALAS_TEXT, LEYES_TEXT, NORMAS_TEXT

class User_state:
    id: int
    name: str = "guest"
    rol: str = "guest"

    def __init__(self, id: int):
        self.id = id

class Health:
    is_submarine_autodestructing: bool = False
    temperatura_interior: int = 23
    soporte_vital: int = 100
    cellar: int = 100
    reactor: int = 100
    exterior: int = 100
    circuits: int = 100
    boiler: int = 100
    gardens: int = 100
    sleeping_quarters: int = 100

class Combustible:
    capacidad: int = 100

class Stock:
    amount: float = 0
    unit: str = "kg"

    def __init__(self, amount: float, unit: str):
        self.amount = amount
        self.unit = unit

class Bot_state:
    health: Health = Health()
    stocks: dict[str, Stock]= {
        'algas': Stock(100, "kg"),
        'proteinas': Stock(10, "kg"),
        'pesca': Stock(4, "kg"),
    }
    users: list[User_state] = []

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
        case 'autodestruccion':
            if state.health.is_submarine_autodestructing == False:
                state.health.is_submarine_autodestructing = True
                return 'Autodestrucción programada para dentro de 30 minutos'
            else:
                return 'Autodestrucción ya había sido iniciada'

        case 'abortar':
            if state.health.is_submarine_autodestructing == True:
                state.health.is_submarine_autodestructing = False
                return 'Autodestrucción abortada'
            else:
                return 'No existe una secuencia de autodestrucción inicializada.'

        case 'consumir':
            state.stocks["algas"].amount = state.stocks["algas"].amount - 2
            return 'Se han consumido 2kg de algas'

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
                - Bodega {state.health.cellar}%\n
                - Reactor {state.health.reactor}%\n
                - Exterior {state.health.exterior}%\n
                - Sistema eléctrico {state.health.circuits}%\n
                - Caldera {state.health.boiler}%\n
                - Huertos {state.health.gardens}%\n
                - Cabinas tripulantes {state.health.sleeping_quarters}%
            """

        case 'inventario':
            inventario = "INVENTARIO DE SUMINISTROS"
            for stock in state.stocks:
                cantidad = state.stocks[stock].amount
                unidad = state.stocks[stock].unit
                msg += f"\n{stock.capitalize()} {cantidad}{unidad}"
            return inventario

        case 'combustible':
            return f"Combustible restante: {0} unidades"

        case _:
            return f"No existe información registrada para la propiedad: {command}."
