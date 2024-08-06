class Atributos:
    ciencia: int = 0
    constitucion: int = 0
    mecanica: int = 0
    pelea: int = 0
    prestigio: int = 0
    programacion: int = 0
    
    @staticmethod
    def from_dict(fuente: dict[str, int]):
        stats = Atributos()
        stats.ciencia = fuente.get('ciencia', 0)
        stats.constitucion = fuente.get('constitucion', 0)
        stats.mecanica = fuente.get('mecanica', 0)
        stats.pelea = fuente.get('pelea', 0)
        stats.prestigio = fuente.get('prestigio', 0)
        stats.programacion = fuente.get('programacion', 0)
        return stats
    
    def to_dict(self):
        return {
            'ciencia': self.ciencia,
            'constitucion': self.constitucion,
            'mecanica': self.mecanica,
            'pelea': self.pelea,
            'prestigio': self.prestigio,
            'programacion': self.programacion,
        }

class Tripulante:
    uuid: str = ""
    id: str = ""
    name: str = ""
    rango: str = ""
    permisos: list[str] = []
    vida: int = 3
    estado: str = ""
    is_sano: bool = True
    is_contagiado: bool = False
    is_criogenizado: bool = False
    atributos: Atributos = Atributos()

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        tripulante = Tripulante()
        tripulante.id = fuente.get('id', 'AH34N')
        tripulante.uuid = fuente.get('uuid', '12314-123125-12264')
        tripulante.name = fuente.get('name', 'unkown')
        tripulante.rango = fuente.get('rango', 'don nadie')
        tripulante.permisos = fuente.get('auth', ['miembro'])
        tripulante.vida = fuente.get('vida', 3)
        tripulante.is_sano = fuente.get('is_sano', True)
        tripulante.is_contagiado = fuente.get('is_contagiado', False)
        tripulante.is_criogenizado = fuente.get('is_criogenizado', False)
        tripulante.atributos = Atributos.from_dict(fuente)
        tripulante.estado = dime_estado(tripulante.vida, tripulante.is_sano, tripulante.is_contagiado, tripulante.is_criogenizado)

        return tripulante
    
    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'rango': self.rango,
            'permisos': self.permisos,
            'vida': self.vida,
            'is_sano': self.is_sano,
            'is_contagiado': self.is_contagiado,
            'is_criogenizado': self.is_criogenizado,
            'atributos': self.atributos.to_dict(),
        }

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
