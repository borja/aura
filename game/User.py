import re

from typing import Optional
from game.Tripulante import Tripulante

class User:
    id: int = -1
    chatId: int = -1
    avatar: Optional[Tripulante] = None

    def __init__(self, id: int):
        self.id = id

    @staticmethod
    def from_dict(fuente: dict[str, any], tripulantes: list[Tripulante]):
        user = User(fuente.get('id', -1))
        tripulanteUuid = fuente.get('avatar', None)
        if tripulanteUuid == None:
            return user
        for tripulante in tripulantes:
            if tripulante.uuid == tripulanteUuid:
                user.avatar = tripulante
                break
        return user
    
    def to_dict(self):
        avatar: None | int = None
        if self.avatar != None:
            avatar = self.avatar.uuid
        return {
            'id': self.id,
            'id': self.chatId,
            'avatar': avatar,
        }
    
    def describe(self):
        if self.avatar == None:
            return f"U({self.id}) [sin rol]"
        
        return f"U({self.id}) [{self.avatar.name}, de {self.avatar.cuerpo}]"
