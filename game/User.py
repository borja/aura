import re

from game.Tripulante import Tripulante
from typing import Optional

class User:
    id: int
    avatar: Optional[Tripulante]

    def __init__(self, id: int):
        self.id = id
