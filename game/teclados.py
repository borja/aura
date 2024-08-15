from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
import time
import json
import math
import consts

from termcolor import colored
from game.Arca import Sala, tiene_permisos
from game.Dialogo import Dialogo
from game.Reto import Reto
from game.User import User
from infra.State import State


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
    """
        Controles sala
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(colored(f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ['Esta sala no existe', None]

    return _loc(state, user, room, '', True)

async def loc_x(state: State, user: User, dialog: Dialogo):
    """
        Cerrar sala
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(colored(f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Esta sala no existe", None]

    return _loc(state, user, room, 'Interacción cerrada. ', False)

async def loc_e(state: State, user: User, dialog: Dialogo):
    """
        Salir de la sala "Exit"
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    if user.avatar is not None:
        user.avatar.sala.ocupantes -= 1
        user.avatar.sala = None

    return _loc(state, user, room, 'Se ha salido de sala. ', False)

async def loc_i(state: State, user: User, dialog: Dialogo):
    """
        Entrar en la sala "get Inside"
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    if user.avatar is not None:
        if user.avatar.sala is not None:
            user.avatar.sala.ocupantes -= 1
        user.avatar.sala = room
        user.avatar.sala.ocupantes += 1

    return _loc(state, user, room, 'Accedido a la sala. ', True)

async def loc_c(state: State, user: User, dialog: Dialogo):
    """
        Cerrar puerta "Close"
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    room.is_puerta_abierta = False

    return _loc(state, user, room, 'Puerta cerrada. ', True)

async def loc_o(state: State, user: User, dialog: Dialogo):
    """
        Abrir puerta "Open"
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    room.is_puerta_abierta = True

    return _loc(state, user, room, 'Puerta abierta. ', True)

async def loc_bo(state: State, user: User, dialog: Dialogo):
    """
        Abrir sello "Block Open"
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    if 'sellable' in room.atributos:
        room.datos["sellado"] = False

    return _loc(state, user, room, 'Sello deshabilitado. ', True)

async def loc_bc(state: State, user: User, dialog: Dialogo):
    """
        Cerrar sello "Block Close"
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    if "sellable" in room.atributos:
        room.is_puerta_abierta = False
        room.datos["sellado"] = True

    return _loc(state, user, room, 'Puerta sellada. ', True)

async def loc_fn(state: State, user: User, dialog: Dialogo):
    """
        Poner la esclusa en neutral "Floodgate Null"
    """
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    if "esclusa" in room.atributos:
        room.is_puerta_abierta = False
        room.datos["modo_esclusa"] = 'NULL'

    return _loc(state, user, room, 'Esclusa ahora en NULL. ', True)

async def loc_fi(state: State, user: User, dialog: Dialogo):
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    if "esclusa" in room.atributos:
        room.datos["modo_esclusa"] = 'INPUT'

    return _loc(state, user, room, 'Esclusa ahora en INPUT. ', True)

async def loc_fo(state: State, user: User, dialog: Dialogo):
    room = next((r for r in state.game.arca.salas if r.id == dialog.data), None)

    if room is None:
        print(
            colored(
                f" ⚠️ {user.describe()} scanned room {dialog.data}. Problem is, it doesn't exist",
                "yellow",
            )
        )
        return ["Esta sala no existe", None]

    if "esclusa" in room.atributos:
        room.datos["modo_esclusa"] = "OUTPUT"

    return _loc(state, user, room, 'Esclusa ahora en OUTPUT. ', True)

async def chl(state: State, user: User, dialog: Dialogo):
    reto = next((r for r in state.game.retos if r.id == dialog.data), None)

    if reto is None:
        print(colored(f" ⚠️ {user.describe()} scanned trial {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Este reto no existe", None]

    return _chl(state, user, reto, '', True)

async def chl_i(state: State, user: User, dialog: Dialogo):
    reto = next((r for r in state.game.retos if r.id == dialog.data), None)

    if reto is None:
        print(colored(f" ⚠️ {user.describe()} tried trial {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Este reto no existe", None]
    intento_text = 'No se puede interactuar sin estar registrado'

    if user.avatar is not None:
        exitos = reto.intentar(user.avatar.atributos)
        print(colored(f" - {user.describe()} tried trial {reto.nombre}. He managed {exitos} successes",'green'))
        intento_text = f"Has conseguido {exitos} éxitos en la prueba"

    return _chl(state, user, reto, intento_text, True)

async def ctl_x(state: State, user: User, dialog: Dialogo):
    reto = next((r for r in state.game.retos if r.id == dialog.data), None)
    
    if reto is None:
        print(colored(f" ⚠️ {user.describe()} closed trial {dialog.data}. Problem is, it doesn't exist",'yellow'))
        return ["Este reto no existe", None]

    return _chl(state, user, reto, 'Interacción cerrada', False)

def _loc(state: State, user: User, sala: Sala, extra: str, haz_botones: bool):
    permisos_usuario = [] if user.avatar is None else user.avatar.permisos
    tiene_permiso_acceso = sala.tiene_permiso(permisos_usuario)
    esta_encerrado = _esta_usuario_encerrado(user)
    estado_especial = ""
    inner_extra = ''

    if esta_encerrado:
        inner_extra = f"Estás encerrado en {user.avatar.sala.nombre}. "

    botones: list[list[InlineKeyboardButton]] | None = None
    if haz_botones:
        botones = []
        special_closure_enablement = True
        special_closure_lock = False
        if 'sellable' in sala.atributos:
            estado_especial += '\nSala sellada' if sala.datos['sellado'] else ''
            if sala.datos['sellado'] is True:
                special_closure_lock = True
                special_closure_enablement = False
            if tiene_permisos(sala.datos["permisos_sellado"], permisos_usuario):
                special_closure_enablement = True
                if sala.datos['sellado'] is True:
                    botones.append(
                        [
                            InlineKeyboardButton(
                                "Liberar sello",
                                callback_data=Dialogo("loc/bo", sala.id).serialize(),
                            )
                        ]
                    )
                else:
                    botones.append(
                        [
                            InlineKeyboardButton(
                                "Sellar",
                                callback_data=Dialogo("loc/bc", sala.id).serialize(),
                            )
                        ]
                    )
        if 'esclusa' in sala.atributos:
            estado_especial += f"\nEstado esclusa: {sala.datos['modo_esclusa']}"
            if sala.datos['modo_esclusa'] != 'INPUT':
                special_closure_lock = True
                special_closure_enablement = False
            if tiene_permisos(sala.datos["permisos_esclusa"], permisos_usuario):
                if sala.datos['modo_esclusa'] == 'INPUT':
                    botones.append(
                        [
                            InlineKeyboardButton(
                                "Esclusa -> NULL",
                                callback_data=Dialogo("loc/fn", sala.id).serialize(),
                            )
                        ]
                    )
                elif sala.datos['modo_esclusa'] == 'NULL':
                    botones.append(
                        [
                            InlineKeyboardButton(
                                "Esclusa -> INPUT",
                                callback_data=Dialogo("loc/fi", sala.id).serialize(),
                            ),
                            InlineKeyboardButton(
                                "Esclusa -> OUTPUT",
                                callback_data=Dialogo("loc/fo", sala.id).serialize(),
                            ),
                        ]
                    )
                else:
                    botones.append(
                        [
                            InlineKeyboardButton(
                                "Esclusa -> NULL",
                                callback_data=Dialogo("loc/fn", sala.id).serialize(),
                            )
                        ]
                    )
        if special_closure_enablement:
            botones_basicos: list[InlineKeyboardButton] = []
            if user.avatar != None and user.avatar.sala != None and sala.id == user.avatar.sala.id:
                botones_basicos.append(
                    InlineKeyboardButton(
                        "Salir", callback_data=Dialogo("loc/e", sala.id).serialize()
                    )
                )
            elif (
                esta_encerrado == False
                and (sala.is_puerta_abierta or tiene_permiso_acceso)
                and sala.ocupantes < sala.aforo
            ):
                botones_basicos.append(
                    InlineKeyboardButton(
                        "Entrar",
                        callback_data=Dialogo("loc/i", sala.id).serialize(),
                    )
                )
            if esta_encerrado == False and tiene_permiso_acceso and "autocerrado" not in sala.atributos:
                if sala.is_puerta_abierta:
                    botones_basicos.append(InlineKeyboardButton('Cerrar Puerta', callback_data=Dialogo('loc/c', sala.id).serialize()))
                elif special_closure_lock is False:
                    botones_basicos.append(
                        InlineKeyboardButton(
                            "Abrir Puerta",
                            callback_data=Dialogo("loc/o", sala.id).serialize(),
                        )
                    )
            if len(botones_basicos) > 0:
                botones.append(botones_basicos)

        botones.append(
            [
                InlineKeyboardButton(
                    "Cerrar Dialogo",
                    callback_data=Dialogo("loc/x", sala.id).serialize(),
                )
            ]
        )

    return [
        state.txts.build_text(
            consts.TXT_SCAN_SALA,
            {
                "nombre_sala": sala.nombre,
                "ocupantes": sala.ocupantes,
                "aforo_sala": sala.aforo,
                "estado": sala.estado,
                "estado_puerta": "Abierta" if sala.is_puerta_abierta else "Cerrada",
                "tiene_permiso": "🟢" if tiene_permiso_acceso else "🛑",
                "estado_especial": estado_especial,
                "descripcion_sala": sala.descripcion,
                "extra": f"{extra}{inner_extra}<i>{time.strftime('%H:%M:%S')}</i>",
            },
        ),
        (InlineKeyboardMarkup(botones) if botones is not None else None),
    ]

def _chl(state: State, user: User, reto: Reto, extra: str, haz_botones: bool):
    markup = None

    if haz_botones and reto.activo and user.avatar is not None and reto.es_capaz(user.avatar.atributos):
        botones = [
            [
                InlineKeyboardButton(
                    "Intentar",
                    callback_data=json.dumps(Dialogo("chl/i", reto.id).to_tuple()),
                )
            ],
            [
                InlineKeyboardButton(
                    "Cerrar",
                    callback_data=json.dumps(Dialogo("chl/x", reto.id).to_tuple()),
                )
            ],
        ]
        markup = InlineKeyboardMarkup(botones)

    text_activo = "" if reto.activo else "\nAhora mismo no se puede hacer nada aquí"

    return [
        state.txts.build_text(
            consts.TXT_SCAN_RETO,
            {
                "nombre_reto": reto.nombre,
                "text_activo": text_activo,
                "descripcion_reto": reto.descripcion,
                "extra": f"{extra}<i>{time.strftime('%H:%M:%S')}</i>",
            },
        ),
        markup,
    ]

def _esta_usuario_encerrado(user: User):
    if user.avatar is None:
        return False
    if user.avatar.sala is None:
        return False
    sala = user.avatar.sala
    if 'sellable' in sala.atributos and sala.datos['sellado']:
        return True
    if 'esclusa' in sala.atributos:
        return sala.datos['modo_esclusa'] != 'INPUT'
    return False
