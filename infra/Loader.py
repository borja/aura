from os import read
from typing import Union
import json

from game.Arca import Stock
from game.Bot import Bot
from game.Tripulante import Atributos, Tripulante
from infra.Settings import Settings

default_load = {
    'chatId': -1,
    'crew': [
        {
            'name': 'AURA',
            'cuerpo': 'IA',
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'sistema',
            'id': 'abf',
            'uuid': 'f0f1104a-5464-40af-88b8-3e3af04a0aa9',
            'permisos': ['admin'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 20,
                'mecanica': 0,
                'combate': 0,
                'credibilidad': 10,
                'programacion': 2
            }
        },
        {
            'name': 'Antón',
            'cuerpo': 'Ingeniería',
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'programador',
            'id': 'DABEST',
            'uuid': 'afecc5fa-42da-455e-802e-05a79e48f1de',
            'permisos': ['mecanico'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 1,
                'mecanica': 2,
                'combate': 0,
                'credibilidad': 0,
                'programacion': 7
            }
        },
        {
            'name': 'Gear',
            'cuerpo': 'Ingeniería',
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'mecanico',
            'id': 'abe',
            'uuid': 'afecc5fa-82da-455e-802e-05a79e48f1de',
            'permisos': ['mecanico'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 1,
                'mecanica': 4,
                'combate': 1,
                'credibilidad': 1,
                'programacion': 3
            }
        },
        {
            'name': 'Max',
            'cuerpo': 'Ingeniería',
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'almirante',
            'id': 'abd',
            'uuid': 'cba92024-b70b-4931-84df-4e6adaa20660',
            'permisos': ['almirante', 'militar', 'cientifico', 'mecanico'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 2,
                'mecanica': 0,
                'combate': 3,
                'credibilidad': 5,
                'programacion': 0
            }
        },
        {
            'name': 'Brute',
            'cuerpo': 'Ingeniería',
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'militar',
            'id': 'abc',
            'uuid': 'fa2562e6-a959-4fc8-b524-162dfe1cd0fc',
            'permisos': ['militar'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 2,
                'mecanica': 2,
                'combate': 4,
                'credibilidad': 2,
                'programacion': 0
            }
        },
        {
            'name': 'Smarty',
            'cuerpo': 'Ingeniería',
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'cientifico',
            'id': 'abg',
            'uuid': 'b233abbe-6219-424c-afff-c11e49a2ba77',
            'permisos': ['cientifico'],
            'attrs': {
                'ciencia': 5,
                'constitucion': 2,
                'mecanica': 0,
                'combate': 1,
                'credibilidad': 2,
                'programacion': 0
            }
        }
    ],
    'arca': {
        'health': {
            'is_fin_del_juego': False,
            'is_arca_autodestructing': False,
            'temperatura_interior': 23,
            'estado_casco': 100
        },
        'stocks': {
            'algolosina': [32,'u']
        },
        'combustible': {
            'capacidad': 100,
            'restante': 20.0,
            'upgraded': False
        },
        'salas': [
            {
                'id': 'T4QRHA',
                'nombre': 'Camarotes',
                'descripcion': '',
                'aforo': 6,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'Q4IQQB',
                'nombre': 'Camarote del Almirantazgo',
                'descripcion': '',
                'aforo': 2,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': ['almirante'],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'ATRPOP',
                'nombre': 'Hospital',
                'descripcion': '',
                'aforo': 3,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': ['sellable'],
                'datos': {
                    'permisos_sellado': ['medico']
                }
            },
            {
                'id': 'EBPJ8Q',
                'nombre': 'Sala de criogenización',
                'descripcion': '',
                'aforo': 2,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': '8UXBNK',
                'nombre': 'Cultivo de Algolosinas I',
                'descripcion': '',
                'aforo': 3,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': '1CFF0T',
                'nombre': 'Cultivo de Algolosinas II',
                'descripcion': '',
                'aforo': 3,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'H2GNP9',
                'nombre': 'Unidad de tratamiento de residuos',
                'descripcion': '',
                'aforo': 1,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': ['mecanico'],
                'atributos': ['autocerrado'],
                'datos': {}
            },
            {
                'id': 'OQENCR',
                'nombre': 'Celda de aislamiento I',
                'descripcion': '',
                'aforo': 1,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': ['sellable'],
                'datos': {
                    'permisos_sellado': ['militar']
                }
            },
            {
                'id': 'IYDE7X',
                'nombre': 'Celda de aislamiento II',
                'descripcion': '',
                'aforo': 1,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': ['sellable'],
                'datos': {
                    'permisos_sellado': ['militar']
                }
            },
            {
                'id': 'MYIMID',
                'nombre': 'Sala de comunicaciones',
                'descripcion': '',
                'aforo': 2,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'NCC4YA',
                'nombre': 'Cámara del reactor',
                'descripcion': '',
                'aforo': 2,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'ZL73LV',
                'nombre': 'Laboratorio de ciencia',
                'descripcion': '',
                'aforo': 3,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': ['cientifico'],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'SNDP9Z',
                'nombre': 'Almacén',
                'descripcion': '',
                'aforo': 1,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'ZR5QA7',
                'nombre': 'Centro de Mando',
                'descripcion': '',
                'aforo': 2,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': ['militar'],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'H1VB2M',
                'nombre': 'Unidad de soporte vital',
                'descripcion': '',
                'aforo': 2,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'RDPI8R',
                'nombre': 'Sala de operaciones',
                'descripcion': '',
                'aforo': 10,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': [],
                'datos': {}
            },
            {
                'id': 'DYHWVI',
                'nombre': 'Esclusa',
                'descripcion': '',
                'aforo': 2,
                'is_puerta_abierta': False,
                'estado': 100,
                'permisos': [],
                'atributos': ['esclusa'],
                'datos': {
                    'modo_esclusa': 'NULL',
                    'permisos_esclusa': ['operador_esclusa']
                }
            }
        ]
    },
    'users': []
}

class Loader:
    save_endpoint: str
    save_method: str
    
    def __init__(self, endpoint: str, method: str):
        self.save_endpoint = endpoint
        self.save_method = method

    def load_into(self, bot: Bot):
        game_dict = _get_dict(self.save_method, self.save_endpoint)

        bot.load(game_dict)

    def save_from(self, bot: Bot):
        game_dict = bot.to_dict()
        _set_dict(self.save_method, self.save_endpoint, game_dict)
        pass


def _get_dict(method: str, endpoint: str):
    if( method != 'file'):
        return default_load
    game_save_txt = ''
    with open(endpoint, mode='r', encoding='utf-8') as handle:
        game_save_txt = handle.read()
    game_save_dict: dict[str, any] = json.loads(game_save_txt)
    return game_save_dict

def _set_dict(method: str, endpoint: str, game_state: dict[str, any]):
    if( method != 'file'):
        return
    with open(endpoint, mode='r+', encoding='utf-8') as handle:
        handle.write(json.dumps(game_state))