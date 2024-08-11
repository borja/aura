
from enum import Enum
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json

DIALOGOS_CONTROL ='ctl'
DIALOGOS_SCAN_SALA = 'sal'
DIALOGOS_RETO = 'ret'

class Dialogo:
    ruta: str = DIALOGOS_CONTROL
    data: any = None

    def __init__(self, ruta: str, data: any = None):
        self.ruta = ruta
        self.data = data

    def clone(self, ruta: str, data: any = None):
        cloned = Dialogo(
            ruta,
            data,
        )
        return cloned

    @staticmethod
    def from_tuple(fuente: tuple[str, str, any]):
        dia = Dialogo(fuente[0], fuente[1])
        return dia

    def to_tuple(self):
        return [
            self.ruta,
            self.data,
        ]

root_control = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Tripulantes", callback_data=json.dumps(Dialogo(f"{DIALOGOS_CONTROL}/crew").to_tuple())),
        InlineKeyboardButton("Arca", callback_data=json.dumps(Dialogo(f"{DIALOGOS_CONTROL}/arca").to_tuple()))
    ],
    [
        InlineKeyboardButton("Retos", callback_data=json.dumps(Dialogo(f"{DIALOGOS_CONTROL}/chl").to_tuple())),
        InlineKeyboardButton("Salas", callback_data=json.dumps(Dialogo(f"{DIALOGOS_CONTROL}/loc").to_tuple()))
    ],
    [
        InlineKeyboardButton('Guardar', callback_data=json.dumps(Dialogo(f"{DIALOGOS_CONTROL}/save").to_tuple())),
        InlineKeyboardButton('Cargar', callback_data=json.dumps(Dialogo(f"{DIALOGOS_CONTROL}/load").to_tuple())),
        InlineKeyboardButton('Cerrar', callback_data=json.dumps(Dialogo(f"{str(DIALOGOS_CONTROL)}/x").to_tuple())),
    ],
])