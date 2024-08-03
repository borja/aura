class Atributos:
    ciencia: int
    constitucion: int
    mecanica: int
    pelea: int
    credibilidad: int
    programacion: int

    def __init__(self, stats: dict):
        self.ciencia = stats.ciencia
        self.constitucion = stats.constitucion
        self.mecanica = stats.mecanica
        self.pelea = stats.pelea
        self.credibilidad = stats.prestigio
        self.programacion = stats.programacion

class Tripulante:
    uuid: str
    name: str
    rango: str
    vida: str
    prestigio: int
    vida: int
    estado: str
    is_enfermo: bool
    atributos: Atributos

    def __init__(self, uuid: str, name: str, rango: str, attrs: Atributos):
        self.uuid = uuid
        self.name = name
        self.rango = rango
        self.vida = 3
        self.estado = "Sano"
        self.is_enfermo = False
        self.attrs = attrs
        self.prestigio = attrs.credibilidad
