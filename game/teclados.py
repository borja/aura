from typing import Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import time
import json
import html
import math
import re

from termcolor import colored
from game.Dialogo import Dialogo
from game.Tripulante import Tripulante
from game.User import User
from infra.State import State
import consts


PAGE_ITEMS = 10
root_control = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Tripulantes", callback_data=json.dumps(Dialogo('ctl/crew').to_tuple())),
        InlineKeyboardButton("Arca", callback_data=json.dumps(Dialogo('ctl/arca').to_tuple()))
    ],
    [
        InlineKeyboardButton("Retos", callback_data=json.dumps(Dialogo('ctl/chl').to_tuple())),
        InlineKeyboardButton("Salas", callback_data=json.dumps(Dialogo('ctl/loc').to_tuple()))
    ],
    [
        InlineKeyboardButton('Guardar', callback_data=json.dumps(Dialogo('ctl/save').to_tuple())),
        InlineKeyboardButton('Cargar', callback_data=json.dumps(Dialogo('ctl/load').to_tuple())),
        InlineKeyboardButton('Cerrar', callback_data=json.dumps(Dialogo('ctl/x').to_tuple())),
    ],
])

async def ctl(state: State, user: User, dialog: Dialogo):
    return ['Control del ARCA', root_control]

async def ctl_x(state: State, user: User, dialog: Dialogo):
    return ['Control finalizado', None]

async def ctl_save(state: State, user: User, dialog: Dialogo):
    state.loader.save_from(state.game)
    return [f"Control del ARCA\n<i>Guardado {time.strftime('%H:%M:%S')}</i>", root_control]

async def ctl_load(state: State, user: User, dialog: Dialogo):
    state.loader.load_into(state.game)
    return [f"Control del ARCA\n<i>Cargado {time.strftime('%H:%M:%S')}</i>", root_control]

async def ctl_crew(state: State, user: User, dialog: Dialogo):
    page = dialog.data if dialog.data != None else 0
    options: list[list[InlineKeyboardButton]] = []

    for i in range(0+(PAGE_ITEMS*page),(PAGE_ITEMS*page)+PAGE_ITEMS):
        if len(state.game.crew) <= i:
            break
        member = state.game.crew[i]
        options.append([InlineKeyboardButton(member.name, callback_data=Dialogo( 'ctl/crew/i', member.id).serialize())])

    mostrando = len(options)
    pages = math.ceil( len(state.game.crew) / PAGE_ITEMS)
    if (pages > 1) or (pages > 0 & mostrando == 0):
        pagesButtons = list(map((lambda i: InlineKeyboardButton(str(i+1), callback_data=Dialogo( 'ctl/crew', i).serialize())), [i for i in range(pages) if i != page]))
        options.append(pagesButtons)
    options.append([InlineKeyboardButton("Atrás", callback_data=json.dumps(dialog.clone('').to_tuple()))])

    return [f"Mostrando {mostrando} tripulantes de {len(state.game.crew)}", InlineKeyboardMarkup(options)]

async def ctl_crew_i(state: State, user: User, dialog: Dialogo):
    tripulante = next((mem for mem in state.game.crew if mem.id == dialog.data), None)
    if tripulante == None:
        return [f"Ha habido un problema para encontrar al tripulante", root_control]
    return ["Ruta crew/i aún no implementada", root_control]

async def ctl_arca(state: State, user: User, dialog: Dialogo):
    return ["Ruta arca aún no implementada", root_control]

async def ctl_chl(state: State, user: User, dialog: Dialogo):
    page = dialog.data if dialog.data != None else 0
    options: list[list[InlineKeyboardButton]] = []

    for i in range(0+(PAGE_ITEMS*page),(PAGE_ITEMS*page)+PAGE_ITEMS):
        if len(state.game.retos) <= i:
            break
        reto = state.game.retos[i]
        options.append([InlineKeyboardButton(reto.nombre, callback_data=Dialogo( 'ctl/chl/i', reto.id).serialize())])

    mostrando = len(options)
    pages = math.ceil( len(state.game.retos) / PAGE_ITEMS)
    if (pages > 1) or (pages > 0 & mostrando == 0):
        pagesButtons = list(map((lambda i: InlineKeyboardButton(str(i+1), callback_data=Dialogo( 'ctl/chl', i).serialize())), [i for i in range(pages) if i != page]))
        options.append(pagesButtons)
    options.append([InlineKeyboardButton("Atrás", callback_data=Dialogo('ctl').serialize())])

    return [f"Mostrando {mostrando} retos de {len(state.game.retos)}", InlineKeyboardMarkup(options)]

async def ctl_chl_i(state: State, user: User, dialog: Dialogo):
    reto = next((reto for reto in state.game.retos if reto.id == dialog.data), None)
    if reto == None:
        return [f"Ha habido un problema para encontrar el reto", root_control]
    return ["Ruta chl/i aún no implementada", root_control]

async def ctl_loc(state: State, user: User, dialog: Dialogo):
    page = dialog.data if dialog.data != None else 0
    options: list[list[InlineKeyboardButton]] = []

    for i in range(0+(PAGE_ITEMS*page),(PAGE_ITEMS*page)+PAGE_ITEMS):
        if len(state.game.arca.salas) <= i:
            break
        sala = state.game.arca.salas[i]
        options.append([InlineKeyboardButton(sala.nombre, callback_data=Dialogo( 'ctl/loc/i', sala.id).serialize())])

    mostrando = len(options)
    pages = math.ceil( len(state.game.arca.salas) / PAGE_ITEMS)
    if (pages > 1) or (pages > 0 & mostrando == 0):
        pagesButtons = list(map((lambda i: InlineKeyboardButton(str(i+1), callback_data=Dialogo( 'ctl/loc', i).serialize())), [i for i in range(pages) if i != page]))
        options.append(pagesButtons)
    options.append([InlineKeyboardButton("Atrás", callback_data=Dialogo('ctl').serialize())])

    return [f"Mostrando {mostrando} salas de {len(state.game.arca.salas)}", InlineKeyboardMarkup(options)]

async def ctl_loc_i(state: State, user: User, dialog: Dialogo):
    sala = next((sala for sala in state.game.arca.salas if sala.id == dialog.data), None)
    if sala == None:
        return [f"Ha habido un problema para encontrar la sala", root_control]
    return ["Ruta loc/i aún no implementada", root_control]

async def msg(state: State, user: User, dialog: Dialogo):
    page = dialog.data if dialog.data != None else 0
    options: list[list[InlineKeyboardButton]] = []

    valid_users = list(g_user for g_user in state.game.users if g_user.avatar != None and g_user.avatar.id != user.avatar.id)
    if len(valid_users) < 1:
        return ["No existe ningún usuario válido para mandar un mensaje", None]

    for i in range(0+(PAGE_ITEMS*page),(PAGE_ITEMS*page)+PAGE_ITEMS):
        if len(valid_users) <= i:
            break
        member = valid_users[i]
        options.append([InlineKeyboardButton(member.avatar.name, callback_data=Dialogo( 'msg/i', member.id).serialize())])

    mostrando = len(options)
    pages = math.ceil( len(valid_users) / PAGE_ITEMS)
    if (pages > 1) or (pages > 0 & mostrando == 0):
        pagesButtons = list(map((lambda i: InlineKeyboardButton(str(i+1), callback_data=Dialogo( 'msg', i).serialize())), [i for i in range(pages) if i != page]))
        options.append(pagesButtons)
    options.append([InlineKeyboardButton("Cancelar", callback_data=json.dumps(Dialogo('msg/x').to_tuple()))])

    return [f"Elige a quien mandar el mensaje.\nMostrando {mostrando} tripulantes disponibles de {len(valid_users)}", InlineKeyboardMarkup(options)]

async def msg_i(state: State, user: User, dialog: Dialogo):
    target_user = next((g_user for g_user in state.game.users if g_user.id == dialog.data), None)
    if target_user == None:
        return ['El usuario parece haberse desconectado', None]
    if target_user.chatId == -1:
        return ["El tripulante no se ha registrado en una terminal válida", None]
    await state.bot.send_message(target_user.chatId, user.outgoing_msg, parse_mode=ParseMode.HTML)
    user.outgoing_msg = ''
    return [f"El mensaje se ha enviado a {target_user.avatar.name}", None]

async def msg_x(state: State, user: User, dialog: Dialogo):
    return ['Se ha cancelado el mensaje', None]

async def mem(state: State, user: User, dialog: Dialogo):
    member = next((mem for mem in state.game.crew if mem.id == dialog.data), None)

    if member is None:
        print(colored(f" ⚠️ {user.describe()} scanned crewmember {dialog.data}. Problem is, he doesn't exist",'yellow'))
        return ["Este tripulante no existe", None]

    return [
        state.txts.build_text(consts.TXT_SCAN_TRIPULANTE, {
            'nombre_tripulante': member.name,
            'cuerpo_tripulante': member.cuerpo,
            'asignacion_tripulante': member.asignacion,
            'prestigio_tripulante': member.prestigio,
            'estado_tripulante': member.estado,
            'extra': f"<i>{time.strftime('%H:%M:%S')}</i>",
        }),
        None
    ]

async def mem_x(state: State, user: User, dialog: Dialogo):
    member = next((mem for mem in state.game.crew if mem.id == dialog.data), None)

    if member is None:
        print(colored(f" ⚠️ {user.describe()} scanned crewmember {dialog.data}. Problem is, he doesn't exist",'yellow'))
        return ["Este tripulante no existe", None]

    return [
        state.txts.build_text(consts.TXT_SCAN_TRIPULANTE, {
            'cuerpo_tripulante': member.name,
            'asignacion_tripulante': member.asignacion,
            'prestigio_tripulante': member.prestigio,
            'estado_tripulante': member.estado,
            'extra': f"Interacción finalizada <i>{time.strftime('%H:%M:%S')}</i>",
        }),
        None
    ]

async def loc(state: State, user: User, dialog: Dialogo):
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(colored(f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Esta sala no existe", None]
    permisos_usuario = [] if user.avatar is None else user.avatar.permisos
    permiso_acceso = room.tiene_permiso(permisos_usuario)
    estado_especial = ''

    return [
        state.txts.build_text(consts.TXT_SCAN_SALA, {
            'nombre_sala': room.nombre,
            'ocupantes': room.ocupantes,
            'aforo_sala': room.aforo,
            'estado': room.estado,
            'estado_puerta': 'Abierta' if room.is_puerta_abierta else 'Cerrada',
            'tiene_permiso': '🟢' if permiso_acceso else '🛑',
            'estado_especial': estado_especial,
            'descripcion_sala': room.descripcion,
            'extra': f"<i>{time.strftime('%H:%M:%S')}</i>",
        }),
        None
    ]

async def loc_x(state: State, user: User, dialog: Dialogo):
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(colored(f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Esta sala no existe", None]
    permisos_usuario = [] if user.avatar is None else user.avatar.permisos
    permiso_acceso = room.tiene_permiso(permisos_usuario)
    estado_especial = ''

    return [
        state.txts.build_text(consts.TXT_SCAN_SALA, {
            'nombre_sala': room.nombre,
            'ocupantes': room.ocupantes,
            'aforo_sala': room.aforo,
            'estado': room.estado,
            'estado_puerta': 'Abierta' if room.is_puerta_abierta else 'Cerrada',
            'tiene_permiso': '🟢' if permiso_acceso else '🛇',
            'estado_especial': estado_especial,
            'descripcion_sala': room.descripcion,
            'extra': f"Interacción finalizada <i>{time.strftime('%H:%M:%S')}</i>",
        }),
        None
    ]

async def chl(state: State, user: User, dialog: Dialogo):
    reto = next((r for r in state.game.retos if r.id == dialog.data), None)
    
    if reto is None:
        print(colored(f" ⚠️ {user.describe()} scanned trial {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Este reto no existe", None]
    text_activo = '' if reto.activo else '\nAhora mismo no puedes hacer nada aquí'
    markup = None

    if reto.activo and user.avatar is not None and reto.es_capaz(user.avatar.atributos):
        botones = [
            [InlineKeyboardButton("Intentar", callback_data=json.dumps(Dialogo("chl/i", dialog.data).to_tuple()))],
            [InlineKeyboardButton("Cerrar", callback_data=json.dumps(Dialogo("chl/x", dialog.data).to_tuple()))],
        ]
        markup = InlineKeyboardMarkup(botones)

    return [
        state.txts.build_text(consts.TXT_SCAN_RETO, {
            'nombre_reto': reto.nombre,
            'text_activo': text_activo,
            'descripcion_reto': reto.descripcion,
            'extra': f"<i>{time.strftime('%H:%M:%S')}</i>",
        }),
        markup
    ]

async def chl_i(state: State, user: User, dialog: Dialogo):
    reto = next((r for r in state.game.retos if r.id == dialog.data), None)
    
    if reto is None:
        print(colored(f" ⚠️ {user.describe()} tried trial {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Este reto no existe", None]
    text_activo = '' if reto.activo else '\nAhora mismo no puedes hacer nada aquí'
    markup = None
    intento_text = 'No se puede interactuar sin estar registrado'

    if user.avatar is not None:
        exitos = reto.intentar(user.avatar.atributos)
        print(colored(f" - {user.describe()} tried trial {reto.nombre}. He managed {exitos} successes",'green'))
        intento_text = f"Has conseguido {exitos} éxitos en la prueba"

    if reto.activo and user.avatar is not None and reto.es_capaz(user.avatar.atributos):
        botones = [
            [InlineKeyboardButton("Intentar", callback_data=json.dumps(Dialogo("chl/i", dialog.data).to_tuple()))],
            [InlineKeyboardButton("Cerrar", callback_data=json.dumps(Dialogo("chl/x", dialog.data).to_tuple()))],
        ]
        markup = InlineKeyboardMarkup(botones)

    return [
        state.txts.build_text(consts.TXT_SCAN_RETO, {
            'nombre_reto': reto.nombre,
            'text_activo': text_activo,
            'descripcion_reto': reto.descripcion,
            'extra': f"{intento_text} <i>{time.strftime('%H:%M:%S')}</i>",
        }),
        markup
    ]

async def ctl_x(state: State, user: User, dialog: Dialogo):
    reto = next((r for r in state.game.retos if r.id == dialog.data), None)
    
    if reto is None:
        print(colored(f" ⚠️ {user.describe()} closed trial {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Este reto no existe", None]
    text_activo = '' if reto.activo else 'Ahora mismo no puedes hacer nada aquí'

    return [
        state.txts.build_text(consts.TXT_SCAN_RETO, {
            'nombre_reto': reto.nombre,
            'text_activo': text_activo,
            'descripcion_reto': reto.descripcion,
            'extra': f"Interacción finalizada <i>{time.strftime('%H:%M:%S')}</i>",
        }),
        None
    ]
