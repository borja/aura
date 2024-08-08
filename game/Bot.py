import re

from typing import Optional
from game.Arca import Arca
from game.Tripulante import Tripulante
from game.User import User
from infra.Texts import Texts

class Bot:
    id: str
    chatId: int = -1
    txts: Texts
    arca: Arca
    crew: list[Tripulante] = []
    users: list[User] = []

    def __init__(self, bot_id: str, arca: Arca, txts: Texts):
        self.id = bot_id
        self.arca = arca
        self.txts = txts

    def user(self, id: int, chatId: Optional[int]):
        for user in self.users:
            if user.id == id:
                if chatId != None:
                    user.chatId = chatId
                return user

        new_user = User(id)
        if chatId != None:
            new_user.chatId = chatId
        self.users.append(new_user)
        return new_user
    
    def load(self, fuente: dict[str, any]):
        self.chatId = fuente.get('chatId', -1)
        self.arca = Arca.from_dict(fuente['arca'])
        crew: list[dict[str, any]] = fuente['crew']
        self.crew = list(map((lambda fuente_crew: Tripulante.from_dict(fuente_crew)), crew))
        users: list[dict[str, any]] = fuente['users']
        self.users = list(map((lambda fuente_users: User.from_dict(fuente_users, self.crew)), users))

    def to_dict(self):
        return {
            'chatId': self.chatId,
            'arca': self.arca.to_dict(),
            'crew': list(map((lambda crew: crew.to_dict()),self.crew)),
            'users': list(map((lambda user: user.to_dict()),self.users)),
        }
