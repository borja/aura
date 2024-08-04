import re

from game.Arca import Arca
from game.Tripulante import Tripulante
from typing import Optional
from game.User import User
from infra.Texts import Texts

class Bot:
    id: str
    txts: Texts
    arca: Arca
    crew: list[Tripulante] = []
    users: list[User] = []

    def __init__(self, bot_id: str, arca: Arca, txts: Texts):
        self.id = bot_id
        self.arca = arca
        self.txts = txts

    def user(self, id: int):
        for user in self.users:
            if user.id == id:
                return user

        new_user = User(id)
        self.users.append(new_user)
        return new_user
