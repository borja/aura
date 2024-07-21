import re

from texts import HELP_TEXT

class User_sate:
    id: int
    name: str = "guest"
    rol: str = "guest"

    def __init__(self, id: int):
        self.id = id

class Health:
    is_submarine_autodestructing: bool = False
    cellar: float = 100
    reactor: float = 100
    exterior: float = 100
    circuits: float = 100
    boiler: float = 100
    gardens: float = 100
    sleeping_quarters: float = 100

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
    users: list[User_sate]

    def user(self, id: int):
        for user in self.users:
            if user.id == id:
                return user

        new_user = User_sate(id)
        self.users.append(new_user)
        return new_user

def help(state: Bot_state, user: User_sate):
    return HELP_TEXT

def run(state: Bot_state, user: User_sate, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')
    if 'autodestruccion' == command:
        if state.health.is_submarine_autodestructing == False:
            state.health.is_submarine_autodestructing = True
            return 'Autodestrucción programada para dentro de 30 minutos'
        else:
            return 'Autodestrucción ya había sido iniciada'
    if 'abortar' == command:
        state.health.is_submarine_autodestructing = False
        return 'Autodestrucción abortada'
    if 'consumir' == command:
        state.stocks["algas"].amount = state.stocks["algas"].amount - 2
        return 'Se han consumido 2kg de algas'
    return f"comando {command} no aceptado, no es un comando ejecutivo registrado"

def say(state: Bot_state, user: User_sate, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')
    if 'estado' == command:
        return f' - Bodega {state.health.cellar}%\n - Reactor {state.health.reactor}%\n - Exterior {state.health.exterior}%\n - Sistema eléctrico {state.health.circuits}%\n - Caldera {state.health.boiler}%\n - Huertos {state.health.gardens}%\n - Cabinas tripulantes {state.health.sleeping_quarters}%'
    if 'inventario' == command:
        msg = ""
        isFirst = True
        for stock in state.stocks:
            if isFirst:
                isFirst = False
                msg += f"{stock.capitalize()} {state.stocks[stock].amount}{state.stocks[stock].unit}"
            else:
                msg += f"\n{stock.capitalize()} {state.stocks[stock].amount}{state.stocks[stock].unit}"
        return msg
    return f"comando {command} no aceptado, no es un comando informativo registrado"
