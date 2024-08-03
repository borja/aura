

class Atributos:
    ciencia: int
    constitucion: int
    mecanica: int
    pelea: int
    prestigio: int
    programacion: int

    def __init__(self, ciencia: int, constitucion: int, mecanica: int, pelea: int, prestigio: int, programacion: int):
        self.ciencia = ciencia
        self.constitucion = constitucion
        self.mecanica = mecanica
        self.pelea = pelea
        self.prestigio = prestigio
        self.programacion = programacion

class Tripulante:
    uuid: str
    name: str
    saludable: bool
    atributos: Atributos

    def __init__(self, uuid: str, saludable: bool, attrs: Atributos):
        self.uuid = uuid
        self.saludable = saludable
        self.attrs = attrs