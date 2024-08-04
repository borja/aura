from os import read
from typing import Union
import json

from game.Arca import Stock
from game.Bot import Bot
from game.Tripulante import Atributos, Tripulante
from infra.Settings import Settings

default_load = {
    "crew": [
        {
            "name": "AURA",
            "vida": 1,
            "is_sano": True,
            "rango": "sistema",
            "uuid": "f0f1104a-5464-40af-88b8-3e3af04a0aa9",
            "auth": ["god"],
            "attrs": {
                "ciencia": 0,
                "constitucion": 20,
                "mecanica": 0,
                "pelea": 0,
                "prestigio": 10,
                "programacion": 2
            }
        },
        {
            "name": "Cyber",
            "vida": 3,
            "is_sano": True,
            "rango": "informatico",
            "uuid": "afecc5fa-82da-455e-802e-05a79e48f1de",
            "auth": ["crew", "engineer"],
            "attrs": {
                "ciencia": 0,
                "constitucion": 1,
                "mecanica": 2,
                "pelea": 0,
                "prestigio": 0,
                "programacion": 7
            }
        },
        {
            "name": "Max",
            "vida": 3,
            "is_sano": True,
            "rango": "almirante",
            "uuid": "cba92024-b70b-4931-84df-4e6adaa20660",
            "auth": ["crew", "admiral", "oficial"],
            "attrs": {
                "ciencia": 0,
                "constitucion": 2,
                "mecanica": 0,
                "pelea": 3,
                "prestigio": 5,
                "programacion": 0
            }
        },
        {
            "name": "Brute",
            "vida": 3,
            "is_sano": True,
            "rango": "militar",
            "uuid": "fa2562e6-a959-4fc8-b524-162dfe1cd0fc",
            "auth": ["crew", "oficial"],
            "attrs": {
                "ciencia": 0,
                "constitucion": 2,
                "mecanica": 2,
                "pelea": 4,
                "prestigio": 2,
                "programacion": 0
            }
        },
        {
            "name": "Smarty",
            "vida": 3,
            "is_sano": True,
            "rango": "cientifico",
            "uuid": "b233abbe-6219-424c-afff-c11e49a2ba77",
            "auth": ["crew", "cientific"],
            "attrs": {
                "ciencia": 5,
                "constitucion": 2,
                "mecanica": 0,
                "pelea": 1,
                "prestigio": 2,
                "programacion": 0
            }
        }
    ],
    "arca": {
        "health": {
            "is_arca_autodestructing": False,
            "temperatura_interior": 23,
        },
        "stocks": {
            "algolosinas": [32,"u"]
        },
        "fuel": {
            "capacidad": 100,
            "restante": 20.0,
            "upgraded": False,
        }
    }
}

class Loader:
    save_endpoint: str
    save_method: str
    
    def __init__(self, endpoint: str, method: str):
        self.save_endpoint = endpoint
        self.save_method = method

    def load_into(self, bot: Bot):
        game_dict = _get_dict(self.save_method, self.save_endpoint)

        arca_dict = game_dict.get("arca", default_load["arca"])

        fuel_dict = arca_dict.get("fuel", default_load["arca"]["fuel"])
        bot.arca.fuel.capacidad = fuel_dict["capacidad"]
        bot.arca.fuel.restante = fuel_dict["restante"]
        bot.arca.fuel.upgraded = fuel_dict["upgraded"]

        health_dict = arca_dict.get("health", default_load["arca"]["health"])
        bot.arca.health.is_arca_autodestructing = health_dict.get("is_arca_autodestructing", default_load["arca"]["health"]["is_arca_autodestructing"])
        bot.arca.health.temperatura_interior = health_dict.get("temperatura_interior", default_load["arca"]["health"]["temperatura_interior"])

        stocks_dict: dict[str, list[any]] = arca_dict.get("stocks", default_load["arca"]["stocks"])
        bot.arca.stocks = {}
        for key, val in stocks_dict.items():
            bot.arca.stocks[key] = Stock(val[0], val[1])


        crew_list = game_dict.get("crew", default_load["crew"])
        for member_dict in crew_list:
            bot.crew.append(Tripulante(member_dict))

    def save_from(self, bot: Bot):
        if( self.save_method != "file"):
            return
        stocks = {}
        for stockName, stockVal in bot.arca.stocks.items:
            stocks[stockName] = [stockVal.amount, stockVal.unit]
        
        crew = []
        for crewmate in bot.crew:
            crew.append({
                "name": crewmate.name,
                "vida": crewmate.vida,
                "is_sano": crewmate.is_sano,
                "is_contagiado": crewmate.is_contagiado,
                "is_criogenizado": crewmate.is_criogenizado,
                "rango": crewmate.rango,
                "uuid": crewmate.uuid,
                "auth": crewmate.permisos,
                "attrs": {
                    "ciencia": crewmate.atributos.ciencia,
                    "constitucion": crewmate.atributos.constitucion,
                    "mecanica": crewmate.atributos.mecanica,
                    "pelea": crewmate.atributos.pelea,
                    "prestigio": crewmate.atributos.prestigio,
                    "programacion": crewmate.atributos.programacion,
                }
            })


        game_dict = {
            "arca": {
                "health": {
                    "is_arca_autodestructing": bot.arca.health.is_arca_autodestructing,
                    "temperatura_interior": bot.arca.health.temperatura_interior,
                    "soporte_vital": bot.arca.health.soporte_vital,
                    "cellar": bot.arca.health.cellar,
                    "reactor": bot.arca.health.reactor,
                    "exterior": bot.arca.health.exterior,
                    "circuits": bot.arca.health.circuits,
                    "boiler": bot.arca.health.boiler,
                    "gardens": bot.arca.health.gardens,
                    "sleeping_quarters": bot.arca.health.sleeping_quarters
                },
                "stocks": stocks,
                "fuel": {
                    "capacidad": bot.arca.fuel.capacidad,
                    "restante": bot.arca.fuel.restante,
                    "upgraded": bot.arca.fuel.upgraded,
                },
            },
            "crew": crew,
        }
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