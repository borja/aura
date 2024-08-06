from os import read
from typing import Union
import json

from game.Arca import Stock
from game.Bot import Bot
from game.Tripulante import Atributos, Tripulante
from infra.Settings import Settings

default_load = {
    'crew': [
        {
            'name': 'AURA',
            'vida': 1,
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'sistema',
            'id': 'abf',
            'uuid': 'f0f1104a-5464-40af-88b8-3e3af04a0aa9',
            'auth': ['god'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 20,
                'mecanica': 0,
                'pelea': 0,
                'prestigio': 10,
                'programacion': 2
            }
        },
        {
            'name': 'Cyber',
            'vida': 3,
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'informatico',
            'id': 'abe',
            'uuid': 'afecc5fa-82da-455e-802e-05a79e48f1de',
            'auth': ['crew', 'engineer'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 1,
                'mecanica': 2,
                'pelea': 0,
                'prestigio': 0,
                'programacion': 7
            }
        },
        {
            'name': 'Max',
            'vida': 3,
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'almirante',
            'id': 'abd',
            'uuid': 'cba92024-b70b-4931-84df-4e6adaa20660',
            'auth': ['crew', 'admiral', 'oficial'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 2,
                'mecanica': 0,
                'pelea': 3,
                'prestigio': 5,
                'programacion': 0
            }
        },
        {
            'name': 'Brute',
            'vida': 3,
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'militar',
            'id': 'abc',
            'uuid': 'fa2562e6-a959-4fc8-b524-162dfe1cd0fc',
            'auth': ['crew', 'oficial'],
            'attrs': {
                'ciencia': 0,
                'constitucion': 2,
                'mecanica': 2,
                'pelea': 4,
                'prestigio': 2,
                'programacion': 0
            }
        },
        {
            'name': 'Smarty',
            'vida': 3,
            'is_sano': True,
            'is_contagiado': False,
            'is_criogenizado': False,
            'rango': 'cientifico',
            'id': 'abg',
            'uuid': 'b233abbe-6219-424c-afff-c11e49a2ba77',
            'auth': ['crew', 'cientific'],
            'attrs': {
                'ciencia': 5,
                'constitucion': 2,
                'mecanica': 0,
                'pelea': 1,
                'prestigio': 2,
                'programacion': 0
            }
        }
    ],
    'arca': {
        'health': {
            'is_arca_autodestructing': False,
            'temperatura_interior': 23,
            'soporte_vital': 100,
            'cellar': 100,
            'reactor': 100,
            'exterior': 100,
            'circuits': 100,
            'boiler': 100,
            'gardens': 100,
            'sleeping_quarters': 100
        },
        'stocks': {
            'algolosinas': [32,'u']
        },
        'fuel': {
            'capacidad': 100,
            'restante': 20.0,
            'upgraded': False
        }
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
    if( method != "file"):
        return default_load
    game_save_txt = ""
    with open(endpoint, mode="r", encoding="utf-8") as handle:
        game_save_txt = handle.read()
    game_save_dict: dict[str, any] = json.loads(game_save_txt)
    return game_save_dict

def _set_dict(method: str, endpoint: str, game_state: dict[str, any]):
    if( method != "file"):
        return
    with open(endpoint, mode="w", encoding="utf-8") as handle:
        handle.write(json.dumps(game_state))