class Atributos:
    ciencia: int
    constitucion: int
    mecanica: int
    combate: int
    programacion: int
    credibilidad: int

    def __init__(self, stats: dict):
        self.ciencia = stats["ciencia"]
        self.constitucion = stats["constitucion"]
        self.mecanica = stats["mecanica"]
        self.combate = stats["combate"]
        self.credibilidad = stats["credibilidad"]
        self.programacion = stats["programacion"]

class Tripulante:
    uuid: str
    id: str
    name: str
    rango: str
    permisos: list[str]
    vida: int
    prestigio: int
    estado: str
    is_sano: bool
    is_contagiado: bool
    is_criogenizado: bool
    atributos: Atributos

    def __init__(self, crewmate: dict):
        self.id = crewmate["id"]
        self.uuid = crewmate["uuid"]
        self.name = crewmate["name"]
        self.rango = crewmate["rango"]
        self.permisos = crewmate["auth"]
        self.vida = crewmate["vida"]
        self.is_sano = crewmate["is_sano"]
        self.is_contagiado = crewmate["is_contagiado"]
        self.is_criogenizado = crewmate["is_criogenizado"]
        self.atributos = Atributos(crewmate["attrs"])
        self.prestigio = self.atributos.credibilidad
        self.estado = dime_estado(self.vida, self.is_sano, self.is_contagiado, self.is_criogenizado)

def dime_estado(vida: int, is_sano: bool, is_contagiado: bool, is_criogenizado: bool):
    if(vida == 0):
        return "Saludando a Cerberos"
    if(is_criogenizado):
        return "Refrigerado"
    if(is_contagiado):
        return "Tiene una tos un poco chunga"
    if(not is_sano):
        return "Habrá recibido una paliza por bocazas"
    return "Está como una rosa"
