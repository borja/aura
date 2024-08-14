from typing import Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import time
import json
import html
import math
import re

from termcolor import colored
from game import teclados
from game.Dialogo import Dialogo
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
                'asignacion_tripulante': user.avatar.asignacion,
                'localizacion_tripulante': 'Pasillos' if user.avatar.sala is None else user.avatar.sala.nombre,
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

async def scan(state: State, user: User, command_text: str) -> tuple[str, Optional[InlineKeyboardMarkup]]:
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:
        case 'crew' | 'tripulante':
            print(colored(f" 🔎 {user.describe()} SCANned crew command: {command} received, with arg: {args[0]}",'blue'))
            return await keyboard_interaction(state, user, Dialogo('mem', args[0]))
        case 'room' | 'sala':
            print(colored(f" 🔎 {user.describe()} SCANned room command: {command} received, with arg: {args[0]}",'blue'))
            return await keyboard_interaction(state, user, Dialogo('loc', args[0]))
        case 'test' | 'analiza':
            print(colored(f" 🔎 {user.describe()} SCANned trial command: {command} received, with arg: {args[0]}",'blue'))
            return await keyboard_interaction(state, user, Dialogo('chl', args[0]))
        case _:
            print(colored(f" ⚠️ - {user.describe()} SCANned unexpected element: {command}",'yellow'))
            return [f"🚫 No es viable realizar un análisis de tipo: {command}", None]

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
        return await keyboard_interaction(state, user, Dialogo('msg', 0))

    avatar_id = avatar_id.lower()
    target_user = next((g_user for g_user in state.game.users if g_user.avatar != None and g_user.avatar.id.lower() == avatar_id), None)
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
    return keyboard_interaction(state, user, Dialogo('ctl'))


async def keyboard_interaction(state: State, user: User, dialog: Dialogo) -> tuple[str, Optional[InlineKeyboardMarkup]]:
    match dialog.ruta:
        case 'ctl':
            return teclados.ctl(state, user, dialog)
        case 'ctl/x':
            return teclados.ctl_x(state, user, dialog)
        case 'ctl/save':
            return teclados.ctl_save(state, user, dialog)
        case 'ctl/load':
            return teclados.ctl_load(state, user, dialog)
        case 'ctl/crew':
            return teclados.ctl_crew(state, user, dialog)
        case 'ctl/crew/i':
            return teclados.ctl_crew_i(state, user, dialog)
        case 'ctl/arca':
            return teclados.ctl_arca(state, user, dialog)
        case 'ctl/chl':
            return teclados.ctl_chl(state, user, dialog)
        case 'ctl/chl/i':
            return teclados.ctl_chl_i(state, user, dialog)
        case 'ctl/loc':
            return teclados.ctl_loc(state, user, dialog)
        case 'ctl/loc/i':
            return teclados.ctl_loc_i(state, user, dialog)
        case 'msg':
            return teclados.msg(state, user, dialog)
        case 'msg/i':
            return teclados.msg_i(state, user, dialog)
        case 'msg/x':
            return teclados.msg_x(state, user, dialog)
        case 'mem':
            return teclados.mem(state, user, dialog)
        case 'mem/x':
            return teclados.mem_x(state, user, dialog)
        case 'loc':
            return teclados.loc(state, user, dialog)
        case 'loc/x':
            return teclados.loc_x(state, user, dialog)
        case 'chl':
            return teclados.chl(state, user, dialog)
        case 'chl/i':
            return teclados.chl_i(state, user, dialog)
        case 'chl/x':
            return teclados.chl_x(state, user, dialog)
        case _:
            return ['Unexpected path', None]

def respuesta_dialogo_textual(state: State, user: User, dialog: Dialogo, text: str):
    user.dialogo = None
    if dialog.data == None:
        return 'Fallo a la hora de determinar qué propiedad cambiar'
    return 'Actualmente no está implementado responder a inputs'