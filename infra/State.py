from telegram import Bot
from game.Game import Game
from infra.Loader import Loader
from infra.Texts import Texts


class State:
    id: str
    loader: Loader
    game: Game
    txts: Texts
    bot: Bot

    def __init__(self, bot_id: str, bot: Bot, loader: Loader, game: Game, txts: Texts):
        self.bot = bot
        self.bot_id = bot_id
        self.loader = loader
        self.game = game
        self.txts = txts