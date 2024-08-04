class Health:
    is_arca_autodestructing: bool = False
    temperatura_interior: int = 23
    estado_casco: float = 100

class Combustible:
    capacidad: int = 100
    restante: float
    upgraded: bool

    def __init__(self, capacidad: int, restante: float, upgraded: bool):
        self.capacidad = capacidad
        self.restante = restante
        self.upgraded = upgraded

class Stock:
    amount: float = 0
    unit: str = "kg"

    def __init__(self, amount: float, unit: str):
        self.amount = amount
        self.unit = unit

class Sala:
    nombre: str
    aforo: int
    estado: int
    permisos: dict

    def __init__(self, nombre: str, aforo: int):
        self.nombre = nombre
        self.aforo = aforo
        self.estado = 100
        self.permisos = {'ciencia': True, 'ingeniería': True, 'militares': True}

class Arca:
    # Estado general
    health: Health = Health()

    # Combustible
    fuel: Combustible = Combustible(100, 100, False)

    # Salas
    sleeping_quarters: Sala = Sala('Camarotes', 6)
    almirante: Sala = Sala('Camarote del Almirantazgo', 2)
    hospital: Sala = Sala('Hospital ', 3)
    soporte_vital: Sala = Sala('Sala de criogenización', 2)
    cultivo1: Sala = Sala('Cultivo de Algolosinas I', 3)
    cultivo2: Sala = Sala('Cultivo de Algolosinas II', 3)
    residuos: Sala = Sala('Unidad de tratamiento de residuos', 1)
    celda1: Sala = Sala('Celda de aislamiento I', 1)
    celda2: Sala = Sala('Celda de aislamiento II', 1)
    comms: Sala = Sala('Sala de comunicaciones', 2)
    reactor: Sala = Sala('Cámara del reactor', 2)
    lab: Sala = Sala('Laboratorio de ciencia', 3)
    almacen: Sala = Sala('Almacén', 1)
    mando: Sala = Sala('Centro de Mando', 2)
    usvital: Sala = Sala('Unidad de soporte vital', 2)
    ops: Sala = Sala('Sala de operaciones', 10)
    esclusa: Sala = Sala('Esclusa', 2)

    # Suministros
    stocks: dict[str, Stock]= {
        'algolosina': Stock(32, "u"),
    }
