
from enum import Enum
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json

DIALOGOS_CONTROL ='ctl'
DIALOGOS_MENSAJE ='msg'
DIALOGOS_SCAN_TRIPULANTE = 'mem'
DIALOGOS_SCAN_SALA = 'loc'
DIALOGOS_SCAN_RETO = 'chl'

class Dialogo:
    ruta: str = DIALOGOS_CONTROL
    data: any = None

    def __init__(self, ruta: str, data: any = None):
        self.ruta = ruta
        self.data = data

    @staticmethod
    def from_tuple(fuente: tuple[str, str, any]):
        dia = Dialogo(fuente[0], fuente[1])
        return dia

    def to_tuple(self):
        return [
            self.ruta,
            self.data,
        ]
    
    def serialize(self):
        return json.dumps(self.to_tuple())