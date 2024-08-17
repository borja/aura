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


_task_reg = re.compile('^([a-z0-9_]+) "((?:[^"]|(?:""))+)"', re.IGNORECASE)
async def orden(state: State, user: User, command_text: str):
    if user.avatar is None:
        return 'Registrate en la terminar antes de intentar asignar permisos'
    if 'admin' not in user.avatar.permisos and 'taskmaster' not in user.avatar.permisos:
        return 'No tienes permiso para designar tareas'
    out_mensaje: list[str] = []
    clean_command = command_text.strip()
    lineas = clean_command.split('\n')
    for linea in lineas:
        mat = _task_reg.match(linea)
        if mat is None:
            out_mensaje.append(f"Linea no válida: '{linea}'")
            continue
        user_id = linea[0:mat.end(1)].lower()
        tarea = linea[mat.start(2):mat.end(2)]

        t_pj = next((t_pj for t_pj in state.game.crew if t_pj.id.lower() == user_id), None)
        if t_pj is None:
            out_mensaje.append(f"Tripulante no válido: '{user_id}'")
            continue

        t_pj.asignacion = tarea

        t_user = next((t_user for t_user in state.game.users if t_user.avatar is not None and t_user.avatar.id == t_pj.id), None)
        if t_user is not None and t_user.chatId != -1:
            await state.bot.send_message(t_user.chatId, f"Se te ha asignado una tarea: {tarea}", parse_mode=ParseMode.HTML)

    return 'Tareas designadas' if len(out_mensaje) < 1 else '\n'.join( out_mensaje)

async def scan(state: State, user: User, command_text: str) -> tuple[str, Optional[InlineKeyboardMarkup]]:
    re_match = re.search("^[^ ]+", command_text.lower())
    command = re_match[0]
    args = command_text[re_match.end(0)+1:].split(' ')

    match command:
        case 'crew' | 'tripulante':
            return await keyboard_interaction(state, user, Dialogo('mem', args[0]))
        case 'room' | 'sala':
            return await keyboard_interaction(state, user, Dialogo('loc', args[0]))
        case 'test' | 'analiza':
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

async def godspeak(state: State, user: User, command_text: str):
    if user.avatar == None or 'god' not in user.avatar.permisos:
        print(colored(f" ⚠️ - {user.describe()} has tried to godspeak",'yellow'))
        return ["No tienes permisos para transmitir tus pensamientos a otras personas, check your privileges, you damn psychic", None]
    
    re_match = re.search("^[^ ]+", command_text.lower())
    avatar_id = re_match[0]
    mensaje_interno = command_text[re_match.end(0)+1:]
    mensaje = mensaje_interno

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
    return [f"Se le ha susurrado a {target_user.avatar.name}", None]

async def controlar(state: State, user: User) -> tuple[str, Optional[InlineKeyboardMarkup]]:
    if user.avatar == None or 'god' not in user.avatar.permisos:
        print(colored(f" ⚠️ - {user.describe()} has tried to take control",'yellow'))
        return [f"Lo siento, no puedo dejarte hacer eso", None]
    print(colored(f" ⚠️ - {user.describe()} has taken control",'blue'))
    return await keyboard_interaction(state, user, Dialogo('ctl'))

async def keyboard_interaction(state: State, user: User, dialog: Dialogo) -> tuple[str, Optional[InlineKeyboardMarkup]]:
    match dialog.ruta:
        case 'ctl':
            return await teclados.ctl(state, user, dialog)
        case 'ctl/x':
            return await teclados.ctl_x(state, user, dialog)
        case 'ctl/save':
            return await teclados.ctl_save(state, user, dialog)
        case 'ctl/load':
            return await teclados.ctl_load(state, user, dialog)
        case 'ctl/crew':
            return await teclados.ctl_crew(state, user, dialog)
        case 'ctl/crew/i':
            return await teclados.ctl_crew_i(state, user, dialog)
        case 'ctl/arca':
            return await teclados.ctl_arca(state, user, dialog)
        case 'ctl/chl':
            return await teclados.ctl_chl(state, user, dialog)
        case 'ctl/chl/i':
            return await teclados.ctl_chl_i(state, user, dialog)
        case 'ctl/loc':
            return await teclados.ctl_loc(state, user, dialog)
        case 'ctl/loc/i':
            return await teclados.ctl_loc_i(state, user, dialog)
        case 'msg':
            return await teclados.msg(state, user, dialog)
        case 'msg/i':
            return await teclados.msg_i(state, user, dialog)
        case 'msg/x':
            return await teclados.msg_x(state, user, dialog)
        case 'mem':
            return await teclados.mem(state, user, dialog)
        case 'mem/x':
            return await teclados.mem_x(state, user, dialog)
        case 'loc':
            return await teclados.loc(state, user, dialog)
        case 'loc/e':
            return await teclados.loc_e(state, user, dialog)
        case 'loc/i':
            return await teclados.loc_i(state, user, dialog)
        case 'loc/c':
            return await teclados.loc_c(state, user, dialog)
        case 'loc/o':
            return await teclados.loc_o(state, user, dialog)
        case 'loc/bc':
            return await teclados.loc_bc(state, user, dialog)
        case 'loc/bo':
            return await teclados.loc_bo(state, user, dialog)
        case 'loc/fn':
            return await teclados.loc_fn(state, user, dialog)
        case 'loc/fi':
            return await teclados.loc_fi(state, user, dialog)
        case 'loc/fo':
            return await teclados.loc_fo(state, user, dialog)
        case 'loc/x':
            return await teclados.loc_x(state, user, dialog)
        case 'chl':
            return await teclados.chl(state, user, dialog)
        case 'chl/i':
            return await teclados.chl_i(state, user, dialog)
        case 'chl/x':
            return await teclados.chl_x(state, user, dialog)
        case _:
            return ['Unexpected path', None]

def respuesta_dialogo_textual(state: State, user: User, dialog: Dialogo, text: str):
    user.dialogo = None
    if dialog.data == None:
        return 'Fallo a la hora de determinar qué propiedad cambiar'
    return 'Actualmente no está implementado responder a inputs'
