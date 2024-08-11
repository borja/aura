from typing import Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import time
import json
import html
import math
import re

from termcolor import colored
from game.Dialogo import Dialogo, DIALOGOS_CONTROL, DIALOGOS_MENSAJE, root_control
from game.User import User
from infra.State import State
import consts

def start(state: State, user: User):
    return state.txts.build_text(consts.TXT_WELCOME)

def help(state: State, user: User):
    return state.txts.build_text(consts.TXT_AYUDA)

def run(state: State, user: User, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:
        case 'autodestrucción' | 'autodestruccion':
            if state.game.arca.health.is_arca_autodestructing is False:
                state.game.arca.health.is_arca_autodestructing = True
                print(colored(f" 🤖 {command} - Autodestrucción INICIADA",'green'))
                return 'Autodestrucción programada para dentro de 30 minutos'
            else:
                print(colored(f" 🤖 {command} - Ya había un proceso en curso",'yellow'))
                return 'Autodestrucción ya había sido iniciada'

        case 'abortar':
            if state.game.arca.health.is_arca_autodestructing:
                state.game.arca.health.is_arca_autodestructing = False
                print(colored(f" 🤖 {command} - Autodestrucción abortada",'green'))
                return 'Autodestrucción abortada'
            else:
                print(colored(f" 🤖 {command} - No existe secuencia de autodestrucción",'yellow'))
                return 'No existe una secuencia de autodestrucción inicializada.'

        case 'consumir':
            state.game.arca.stocks["algolosina"].amount -= 1
            print(colored(f" 🤖 {command} - 1 algolosina. Restantes: {state.game.arca.stocks["algolosina"].amount}",'green'))
            return 'Se han consumido 1 algolosina'

        case _:
            print(colored(f" ⚠️ - Invalid command request: {command}",'yellow'))
            return f"El comando: '{command}' no está implementado en la interfaz AURA"

def print_estado(state: State):
    vida = state.game.arca.health
    auto_destr_msg = '⏲️ Programada' if vida.is_arca_autodestructing else '✅ Inactiva'
    return state.txts.build_text(consts.TXT_ESTADO, {
        'temperatura': vida.temperatura_interior,
        'auto_destr_msg': auto_destr_msg,
        'estado_casco': vida.estado_casco,
    })

def say(state: State, user: User, command_text: str):
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

        case 'estado' | 'st' | 'nave' | 'arca':
            print(colored(f" 🤖 {command} - Estado del ARCA",'green'))
            return print_estado(state)

        case 'inventario' | 'inv' | 'stock':
            inventario = "INVENTARIO DE SUMINISTROS"
            for stock in state.game.arca.stocks:
                cantidad = state.game.arca.stocks[stock].amount
                unidad = state.game.arca.stocks[stock].unit
                inventario += f"\n{stock.capitalize()} {cantidad}{unidad}"
            print(colored(f" 🤖 {command} - Inventario",'green'))
            return inventario

        case 'combustible' | 'fuel' | 'carburante':
            print(colored(f" 🤖 {command} - Restante: {state.game.arca.combustible.restante}",'green'))
            return f"Combustible restante: {state.game.arca.combustible.restante} unidades"

        case _:
            print(colored(f" ⚠️ - Invalid information request: {command}",'yellow'))
            return f"No existe información registrada para la propiedad: {command}"

def describe_crew(state: State, user: User, tripulante):
    member = next((mem for mem in state.game.crew if mem.id == tripulante), None)

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

def describe_room(state: State, user: User, sala):
    room = next((r for r in state.game.arca.salas if r.id == sala), None)

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

def scan(state: State, user: User, command_text: str):
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

def register(state: State, user: User, command_text: str):
    re_match = re.search("^[^ ]+", command_text.lower())
    id_registro = re_match[0]

    avatar = next((avatar for avatar in state.game.crew if avatar.uuid == id_registro), None)
    if avatar == None:
        print(colored(f" ⚠️ WARNING: Register with id {id_registro} failed",'yellow'))
        return f"No exite ningún tripulante con la id indicada"

    user.avatar = avatar
    return state.txts.build_text(consts.TXT_SALUDO, {
        'nombre_tripulante': avatar.name,
    })

async def broadcast(state: State, user: User, command_text: str):
    if user.avatar == None or ('admin' not in user.avatar.permisos and 'god' not in user.avatar.permisos and 'radiohost' not in user.avatar.permisos):
        print(colored(f" ⚠️ - {user.describe()} has tried to broadcast",'yellow'))
        return "No tienes permisos para mandar un comunicado a toda la nave"
    
    mensaje = state.txts.build_text(consts.TXT_BROADCAST, {
        'nombre_tripulante': user.avatar.name,
        'mensaje': html.escape(command_text),
    })

    for target_user in state.game.users:
        if target_user.avatar == None or user.avatar.id == target_user.avatar.id:
            continue
        if target_user.chatId == -1:
            continue
        await state.bot.send_message(target_user.chatId, mensaje, parse_mode=ParseMode.HTML)

    return 'Transmisión emitida'

async def enviar_mensaje(state: State, user: User, command_text: str) -> tuple[str, Optional[InlineKeyboardMarkup]]:
    if user.avatar == None or ('admin' not in user.avatar.permisos and 'god' not in user.avatar.permisos and 'whisperer' not in user.avatar.permisos):
        print(colored(f" ⚠️ - {user.describe()} has tried to whisper",'yellow'))
        return ["No tienes permisos para mandar enviar mensajes a otros tripulantes", None]
    
    re_match = re.search("^[^ ]+", command_text.lower())
    avatar_id = re_match[0]
    mensaje_interno = command_text[re_match.end(0)+1:]
    mensaje = state.txts.build_text(consts.TXT_MENSAJE, {
        'nombre_tripulante': user.avatar.name,
        'mensaje': html.escape(mensaje_interno),
    })

    if avatar_id == '?':
        user.outgoing_msg = mensaje
        return await keyboard_interaction(state, user, Dialogo(DIALOGOS_MENSAJE, 0))

    target_user = next((g_user for g_user in state.game.users if g_user.avatar != None and g_user.avatar.id == avatar_id), None)
    if target_user == None:
        return ["No se ha podido encontrar el tripulante", None]
    if target_user.chatId == -1:
        return ["El tripulante no se ha registrado en una terminal válida", None]

    await state.bot.send_message(target_user.chatId, mensaje, parse_mode=ParseMode.HTML)
    return [f"Mensaje transmitido a {target_user.avatar.name}", None]


def controlar(state: State, user: User) -> tuple[str, Optional[InlineKeyboardMarkup]]:
    if user.avatar == None or 'god' not in user.avatar.permisos:
        print(colored(f" ⚠️ - {user.describe()} has tried to take control",'yellow'))
        return [f"Lo siento, no puedo dejarte hacer eso", None]
    print(colored(f" ⚠️ - {user.describe()} has taken control",'blue'))
    return ['Control del ARCA', root_control]


PAGE_ITEMS = 10
async def keyboard_interaction(state: State, user: User, dialog: Dialogo) -> tuple[str, Optional[InlineKeyboardMarkup]]:
    match dialog.ruta:
        case 'ctl':
            return ['Control del ARCA', root_control]
        case 'ctl/x':
            return ['Control finalizado', None]
        case 'ctl/save':
            state.loader.save_from(state.game)
            return [f"Control del ARCA\n<i>Guardado {time.time()}</i>", root_control]
        case 'ctl/load':
            state.loader.load_into(state.game)
            return [f"Control del ARCA\n<i>Cargado {time.time()}</i>", root_control]
        case 'ctl/crew':
            page = dialog.data if dialog.data != None else 0
            options: list[list[InlineKeyboardButton]] = []

            for i in range(0+(PAGE_ITEMS*page),(PAGE_ITEMS*page)+PAGE_ITEMS):
                if len(state.game.crew) <= i:
                    break
                member = state.game.crew[i]
                options.append([InlineKeyboardButton(member.name, callback_data=json.dumps(dialog.clone(f"{DIALOGOS_CONTROL}/crew/i", member.id).to_tuple()))])

            mostrando = len(options)
            pages = math.ceil( len(state.game.crew) / PAGE_ITEMS)
            if (pages > 1) or (pages > 0 & mostrando == 0):
                pagesButtons = list(map((lambda i: InlineKeyboardButton(str(i+1), callback_data=json.dumps(dialog.clone(f"{DIALOGOS_CONTROL}/crew", i).to_tuple()))), [i for i in range(pages) if i != page]))
                options.append(pagesButtons)
            options.append([InlineKeyboardButton("Atrás", callback_data=json.dumps(dialog.clone('').to_tuple()))])

            return [f"Mostrando {mostrando} tripulantes de {len(state.game.crew)}", InlineKeyboardMarkup(options)]
        case 'ctl/crew/i':
            tripulante = next((mem for mem in state.game.crew if mem.id == dialog.data), None)
            if tripulante == None:
                return [f"Ha habido un problema para encontrar al tripulante", root_control]
            return ["Ruta crew/i aún no implementada", root_control]
        case 'ctl/arca':
            return ["Ruta arca aún no implementada", root_control]
        case 'ctl/chl':
            page = dialog.data if dialog.data != None else 0
            options: list[list[InlineKeyboardButton]] = []

            for i in range(0+(PAGE_ITEMS*page),(PAGE_ITEMS*page)+PAGE_ITEMS):
                if len(state.game.retos) <= i:
                    break
                reto = state.game.retos[i]
                options.append([InlineKeyboardButton(reto.nombre, callback_data=json.dumps(dialog.clone(f"{DIALOGOS_CONTROL}/chl/i", reto.id).to_tuple()))])

            mostrando = len(options)
            pages = math.ceil( len(state.game.retos) / PAGE_ITEMS)
            if (pages > 1) or (pages > 0 & mostrando == 0):
                pagesButtons = list(map((lambda i: InlineKeyboardButton(str(i+1), callback_data=json.dumps(dialog.clone(f"{DIALOGOS_CONTROL}/chl", i).to_tuple()))), [i for i in range(pages) if i != page]))
                options.append(pagesButtons)
            options.append([InlineKeyboardButton("Atrás", callback_data=json.dumps(dialog.clone('').to_tuple()))])

            return [f"Mostrando {mostrando} retos de {len(state.game.retos)}", InlineKeyboardMarkup(options)]
        case 'ctl/chl/i':
            reto = next((reto for reto in state.game.retos if reto.id == dialog.data), None)
            if reto == None:
                return [f"Ha habido un problema para encontrar el reto", root_control]
            return ["Ruta chl/i aún no implementada", root_control]
        case 'ctl/loc':
            page = dialog.data if dialog.data != None else 0
            options: list[list[InlineKeyboardButton]] = []

            for i in range(0+(PAGE_ITEMS*page),(PAGE_ITEMS*page)+PAGE_ITEMS):
                if len(state.game.arca.salas) <= i:
                    break
                sala = state.game.arca.salas[i]
                options.append([InlineKeyboardButton(sala.nombre, callback_data=json.dumps(dialog.clone(f"{DIALOGOS_CONTROL}/loc/i", sala.id).to_tuple()))])

            mostrando = len(options)
            pages = math.ceil( len(state.game.arca.salas) / PAGE_ITEMS)
            if (pages > 1) or (pages > 0 & mostrando == 0):
                pagesButtons = list(map((lambda i: InlineKeyboardButton(str(i+1), callback_data=json.dumps(dialog.clone(f"{DIALOGOS_CONTROL}/loc", i).to_tuple()))), [i for i in range(pages) if i != page]))
                options.append(pagesButtons)
            options.append([InlineKeyboardButton("Atrás", callback_data=json.dumps(dialog.clone('').to_tuple()))])

            return [f"Mostrando {mostrando} salas de {len(state.game.arca.salas)}", InlineKeyboardMarkup(options)]
        case 'ctl/loc/i':
            sala = next((sala for sala in state.game.arca.salas if sala.id == dialog.data), None)
            if sala == None:
                return [f"Ha habido un problema para encontrar la sala", root_control]
            return ["Ruta loc/i aún no implementada", root_control]
        case 'msg':
            page = dialog.data if dialog.data != None else 0
            options: list[list[InlineKeyboardButton]] = []

            valid_users = list(g_user for g_user in state.game.users if g_user.avatar != None and g_user.avatar.id != user.avatar.id)
            if len(valid_users) < 1:
                return ["No existe ningún usuario válido para mandar un mensaje", None]

            for i in range(0+(PAGE_ITEMS*page),(PAGE_ITEMS*page)+PAGE_ITEMS):
                if len(valid_users) <= i:
                    break
                member = valid_users[i]
                options.append([InlineKeyboardButton(member.avatar.name, callback_data=json.dumps(Dialogo(f"{DIALOGOS_MENSAJE}/i", member.id).to_tuple()))])

            mostrando = len(options)
            pages = math.ceil( len(valid_users) / PAGE_ITEMS)
            if (pages > 1) or (pages > 0 & mostrando == 0):
                pagesButtons = list(map((lambda i: InlineKeyboardButton(str(i+1), callback_data=json.dumps(Dialogo(f"{DIALOGOS_MENSAJE}", i).to_tuple()))), [i for i in range(pages) if i != page]))
                options.append(pagesButtons)
            options.append([InlineKeyboardButton("Cancelar", callback_data=json.dumps(Dialogo(f"{DIALOGOS_MENSAJE}/x").to_tuple()))])

            return [f"Elige a quien mandar el mensaje.\nMostrando {mostrando} tripulantes disponibles de {len(valid_users)}", InlineKeyboardMarkup(options)]
        case 'msg/i':
            target_user = next((g_user for g_user in state.game.users if g_user.id == dialog.data), None)
            if target_user == None:
                return ['El usuario parece haberse desconectado', None]
            if target_user.chatId == -1:
                return ["El tripulante no se ha registrado en una terminal válida", None]
            await state.bot.send_message(target_user.chatId, user.outgoing_msg, parse_mode=ParseMode.HTML)
            user.outgoing_msg = ''
            return [f"El mensaje se ha enviado a {target_user.avatar.name}", None]
        case 'msg/x':
            return ['Se ha cancelado el mensaje', None]
        case _:
            return ['Unexpected path', None]

def respuesta_dialogo_textual(state: State, user: User, dialog: Dialogo, text: str):
    user.dialogo = None
    if dialog.data == None:
        return 'Fallo a la hora de determinar qué propiedad cambiar'
    return 'Actualmente no está implementado responder a inputs'