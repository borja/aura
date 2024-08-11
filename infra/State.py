from game.Game import Game
from infra.Loader import Loader
from infra.Texts import Texts


class State:
    id: str
    loader: Loader
    game: Game
    txts: Texts

    def __init__(self, bot_id: str, loader: Loader, game: Game, txts: Texts):
        self.bot_id = bot_id
        self.loader = loader
        self.game = game
        self.txts = txts