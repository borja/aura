class Atributos:
    ciencia: int = 0
    combate: int = 0
    constitucion: int = 0
    credibilidad: int = 0
    mecanica: int = 0
    programacion: int = 0
    
    @staticmethod
    def from_dict(fuente: dict[str, int]):
        stats = Atributos()
        stats.ciencia = fuente.get('ciencia', 0)
        stats.combate = fuente.get('combate', 0)
        stats.credibilidad = fuente.get('credibilidad', 0)
        stats.constitucion = fuente.get('constitucion', 0)
        stats.mecanica = fuente.get('mecanica', 0)
        stats.programacion = fuente.get('programacion', 0)
        return stats
    
    def to_dict(self):
        return {
            'ciencia': self.ciencia,
            'combate': self.combate,
            'credibilidad': self.credibilidad,
            'constitucion': self.constitucion,
            'mecanica': self.mecanica,
            'programacion': self.programacion,
        }

class Tripulante:
    uuid: str = ''
    id: str = ''
    name: str = ''
    cuerpo: str = ''
    rango: str = ''
    permisos: list[str] = []
    vida: int = 3
    estado: str = ''
    is_sano: bool = True
    is_contagiado: bool = False
    is_criogenizado: bool = False
    atributos: Atributos = Atributos()

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        tripulante = Tripulante()
        tripulante.id = fuente.get('id', 'ERR500')
        tripulante.uuid = fuente.get('uuid', 'ERR500-ERR500-ERR500')
        tripulante.name = fuente.get('name', 'ERR500')
        tripulante.cuerpo = fuente.get('cuerpo', 'ERR500')
        tripulante.rango = fuente.get('rango', 'ERR500')
        tripulante.permisos = fuente.get('permisos', ['miembro'])
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
            'cuerpo': self.cuerpo,
            'rango': self.rango,
            'permisos': self.permisos,
            'vida': self.vida,
            'is_sano': self.is_sano,
            'is_contagiado': self.is_contagiado,
            'is_criogenizado': self.is_criogenizado,
            'atributos': self.atributos.to_dict(),
        }

def dime_estado(vida: int, is_sano: bool, is_contagiado: bool, is_criogenizado: bool):
    if vida < 0:
        return '💀 MUERTO'
    if is_criogenizado:
        return '❄️ CRIOGENIZADO'
    if is_contagiado:
        return '☣️ INFECTADO'
    if not is_sano:
        return '😓 DÉBIL'
    return '💚 SANO'
