class Health:
    is_fin_del_juego: bool = False
    is_arca_autodestructing: bool = False
    temperatura_interior: int = 23
    estado_casco: float = 100

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        health = Health()
        health.is_fin_del_juego = fuente.get('is_fin_del_juego', False)
        health.is_arca_autodestructing = fuente.get('is_arca_autodestructing', False)
        health.temperatura_interior = fuente.get('temperatura_interior', 23)
        health.estado_casco = fuente.get('estado_casco', 100)
        return health
    
    def to_dict(self):
        return {
            'is_fin_del_juego': self.is_fin_del_juego,
            'is_arca_autodestructing': self.is_arca_autodestructing,
            'temperatura_interior': self.temperatura_interior,
            'estado_casco': self.temperatura_interior,
        }

class Combustible:
    capacidad: int = 100
    restante: float
    upgraded: bool

    def __init__(self, capacidad: int, restante: float, upgraded: bool):
        self.capacidad = capacidad
        self.restante = restante
        self.upgraded = upgraded

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        out_combustible = Combustible(fuente.get('capacidad', 100), fuente.get('restante', 100.0), fuente.get('upgraded', False))
        return out_combustible
    
    def to_dict(self):
        return {
            'capacidad': self.capacidad,
            'restante': self.restante,
            'upgraded': self.upgraded,
        }

class Stock:
    amount: float = 0
    unit: str = 'kg'

    def __init__(self, amount: float, unit: str):
        self.amount = amount
        self.unit = unit
    
    @staticmethod
    def from_tuple(tuple: tuple[int, str]):
        return Stock(tuple[0], tuple[1])
    
    def to_tuple(self):
        return (self.amount, self.unit)

class Sala:
    id: str
    nombre: str
    aforo: int
    estado: int
    permisos: list[str]

    def __init__(self, nombre: str, aforo: int):
        self.nombre = nombre
        self.aforo = aforo
        self.estado = 100
        self.permisos = []

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        out_sala = Sala('', 1)
        out_sala.id = fuente.get('id', 'ERR500__invalid_id')
        out_sala.nombre = fuente.get('nombre', 'ERR500__invalid_name')
        out_sala.aforo = fuente.get('aforo', 1)
        out_sala.estado = fuente.get('estado', 100)
        out_sala.permisos = fuente.get('permisos', [])
        return out_sala
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'aforo': self.aforo,
            'estado': self.estado,
            'permisos': self.permisos,
        }

class Esclusa(Sala):
    is_output_open: bool = False
    is_input_open: bool = False

    def status(self):
        if self.is_input_open is True:
            return 'INPUT'
        elif self.is_output_open is True:
            return 'OUPUT'
        else:
            return 'NULL'

    def open_input(self):
        if self.is_input_open is True:
            print(colored(" ⚠️ - ESCLUSA-INPUT is already OPEN",'yellow'))
            return '⚠️ La esclusa INPUT ya estaba abierta'
        else:
            if self.is_output_open is True:
                print(colored(" ⚠️ - ESCLUSA-OUTPUT is OPEN, cannot open INPUT",'yellow'))
                return '🚫 No se ha podido realizar: La esclusa OUTPUT está abierta'
            else:
                self.is_input_open = True
                print(colored(' 🤖 ESCLUSA: input abierto','green'))
                return '↪️ ESCLUSA INPUT ABIERTA'
        
    def open_output(self):
        if self.is_output_open is True:
            print(colored(" ⚠️ - ESCLUSA-OUTPUT is already OPEN",'yellow'))
            return '⚠️ La esclusa OUTPUT ya estaba abierta'
        else:
            if self.is_input_open is True:
                print(colored(" ⚠️ - ESCLUSA-INTPUT is OPEN, cannot open OUTPUT",'yellow'))
                return '🚫 No se ha podido realizar: La esclusa INPUT está abierta'
            else:
                self.is_output_open = True
                print(colored(' 🤖 ESCLUSA: output abierto','green'))
                return '↪️ ESCLUSA OUTPUT ABIERTA'

    def close_input(self):
        if self.is_input_open is False:
            print(colored(" ⚠️ - ESCLUSA-INPUT is already CLOSED",'yellow'))
            return '⚠️ La esclusa INPUT ya estaba cerrada'
        else:
            self.is_input_open = False
            print(colored(" 🤖 ESCLUSA-INPUT cerrada",'green'))
            return '↪️ ESCLUSA INPUT CERRADA'

    def close_output(self):
        if self.is_output_open is False:
            print(colored(" ⚠️ - ESCLUSA-OUTPUT is already CLOSED",'yellow'))
            return '⚠️ La esclusa OUTPUT ya estaba cerrada'
        else:
            self.is_output_open = False
            print(colored(" 🤖 ESCLUSA-OUTPUT cerrada",'green'))
            return '↪️ ESCLUSA OUTPUT CERRADA'
    
    @staticmethod
    def from_dict(fuente: dict[str, any]):
        esclusa = Esclusa()
        esclusa.is_output_open = fuente.get('is_output_open', False)
        esclusa.is_input_open = fuente.get('is_input_open', False)
        return esclusa
    
    def to_dict(self):
        dict_esclusa = super().to_dict()
        dict_esclusa["is_output_open"] = False
        dict_esclusa["is_input_open"] = False
        return dict_esclusa

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
    esclusa: Esclusa = Esclusa('Esclusa', 2)

    # Suministros
    stocks: dict[str, Stock]= {
        'algolosina': Stock(32, "u"),
    }

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        arca = Arca()
        return arca

    def to_dict(self):
        stocks = dict[str, dict[str, tuple[int, str]]]
        for stock, value in self.stocks.items():
            stocks[stock] = value.to_tuple()
        return {
            'health': self.health.to_dict(),
            'fuel': self.fuel.to_dict(),
            'stocks': stocks,
        }
