import re

from typing import Optional
from game.Tripulante import Tripulante

class User:
    id: int
    avatar: Optional[Tripulante]

    def __init__(self, id: int):
        self.id = id
