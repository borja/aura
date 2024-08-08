import re

from termcolor import colored
from game.Bot import Bot
from game.User import User
import consts

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

def print_estado(state: Bot):
    vida = state.arca.health
    auto_destr_msg = '⏲️ Programada' if vida.is_arca_autodestructing else '✅ Inactiva'
    return state.txts.build_text(consts.TXT_ESTADO, {
        'temperatura': vida.temperatura_interior,
        'auto_destr_msg': auto_destr_msg,
        'estado_casco': vida.estado_casco,
    })

def say(state: Bot, user: User, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:
        case 'sobremi' | 'salud' | 'yo' | 'me' | 'mi' | 'yo?':
            print(colored(f" 🤖 {command} - {user.describe()} asked about himself",'green'))
            if user.avatar == None:
                return 'Aún no has hecho login al sistema'
            return state.txts.build_text(consts.TXT_DETALLE_TRIPULANTE, {
                'nombre': user.avatar.name,
                'puntos_vida': user.avatar.vida,
                'estado': user.avatar.estado,
                'cuerpo': user.avatar.cuerpo,
                'rango': user.avatar.rango,
                'permisos': str.join(', ', user.avatar.permisos),
                'ciencia': user.avatar.atributos.ciencia,
                'combate': user.avatar.atributos.combate,
                'constitucion': user.avatar.atributos.constitucion,
                'credibilidad': user.avatar.atributos.credibilidad,
                'mecanica': user.avatar.atributos.mecanica,
                'programacion': user.avatar.atributos.programacion,
            })

        case 'tripulacion' | 'tripulantes' | 'tripu' | 'crew':
            print(colored(f" 🤖 {command} - lista de tripulantes",'green'))
            return state.txts.build_text(consts.TXT_TRIPULANTES)

        case 'salas' | 'dependencias' | 'aforo' | 'sala':
            print(colored(f" 🤖 {command} - lista de salas",'green'))
            return state.txts.build_text(consts.TXT_SALAS)

        case 'leyes' | 'LGJ6' | 'maximas':
            print(colored(f" 🤖 {command} - lista de Leyes",'green'))
            return state.txts.build_text(consts.TXT_LEYES)

        case 'normas' | 'normativa' | 'reglas' | 'reglamento':
            print(colored(f" 🤖 {command} - lista de Reglas",'green'))
            return state.txts.build_text(consts.TXT_NORMAS)

        case 'estado' | 'st' | 'nave':
            print(colored(f" 🤖 {command} - Estado del ARCA",'green'))
            return print_estado(state)

        case 'inventario' | 'inv':
            inventario = "INVENTARIO DE SUMINISTROS"
            for stock in state.arca.stocks:
                cantidad = state.arca.stocks[stock].amount
                unidad = state.arca.stocks[stock].unit
                inventario += f"\n{stock.capitalize()} {cantidad}{unidad}"
            print(colored(f" 🤖 {command} - Inventario",'green'))
            return inventario

        case 'combustible' | 'fuel' | 'carburante':
            print(colored(f" 🤖 {command} - Restante: {state.arca.combustible.restante}",'green'))
            return f"Combustible restante: {state.arca.combustible.restante} unidades"

        case _:
            print(colored(f" ⚠️ - Invalid information request: {command}",'yellow'))
            return f"No existe información registrada para la propiedad: {command}"

def describe_crew(state: Bot, user: User, tripulante):
    member = next((mem for mem in state.crew if mem.id == tripulante), None)

    if member is None:
        print(colored(f" ⚠️ El tripulante: {tripulante} no existe",'yellow'))
        return "Este tripulante no existe"
    else:
        print(colored(f" 🤖 SCAN - Resultado del tripulante: {member.name}",'green'))
        return f"""
*INFORME DE TRIPULANTE*

    *Nombre*: {member.name}
    *Cuerpo*: {member.cuerpo}
    *Asignación*: {member.rango}
    *Prestigio* {member.prestigio}
    *Salud*: {member.estado}
    """

def describe_room(state: Bot, user: User, sala):
    room = next((r for r in state.arca.salas if r.id == sala), None)

    if room is None:
        print(colored(f" ⚠️ La sala: {room} no existe",'yellow'))
        return "⚠️ La sala introducida no existe"
    else:
        print(colored(f" 🤖 SCAN - Resultado de la sala: {room.nombre}",'green'))
        return f"""
**{room.nombre}**
Descripción: {room.descripcion}
Aforo: {room.aforo} tripulantes
"""

def scan(state: Bot, user: User, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:
        case 'crew' | 'tripulante':
            print(colored(f" 🔎 SCAN CODE command: {command} received, with args: ",'blue'))
            return describe_crew(state, user, args[0])
        case 'room' | 'sala':
            print(colored(f" ⚠️ WARNING: SCAN feature for command: {command}, {args} is being implemented",'yellow'))
            return describe_room(state, user, args[0])
        case 'test' | 'analiza':
            print(colored(f" ⚠️ WARNING: SCAN feature for command: {command}, {args} is not implemented",'yellow'))
            return " ⚠️ WARNING: Esta feature no ha sido implementada"
        case _:
            print(colored(f" ⚠️ - Invalid scan request: {command}",'yellow'))
            return f"🚫 No es viable realizar un análisis de tipo: {command}"            

def register(state: Bot, user: User, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    id_registro = re_match[0]

    avatar = next((avatar for avatar in state.crew if avatar.uuid == id_registro), None)
    if avatar == None:
        print(colored(f" ⚠️ WARNING: Register with id {id_registro} failed",'yellow'))
        return f"No exite ningún tripulante con la id indicada"

    user.avatar = avatar
    return state.txts.build_text(consts.TXT_SALUDO, {
        'nombre_tripulante': avatar.name,
    })
