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

ATR_ESCLUSA = 'esclusa'
ATR_SELLABLE = 'sellable'
ATR_AUTOCERRADO = 'autocerrado'

class Sala:
    id: str = ''
    nombre: str = ''
    descripcion: str = ''
    aforo: int = 1
    is_puerta_abierta: bool = False
    estado: int = 100
    permisos: list[str] = []
    atributos: list[str] = []
    datos: dict[str, any] = dict()

    def __init__(self, nombre: str, aforo: int):
        self.nombre = nombre
        self.aforo = aforo

    def tiene_permiso(self, permisos: list[str]):
        if permisos[0] == 'admin':
            return True
        for requisito in self.permisos:
            if requisito not in permisos:
                return False
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'aforo': self.aforo,
            'is_puerta_abierta': self.is_puerta_abierta,
            'estado': self.estado,
            'permisos': self.permisos,
            'atributos': self.atributos,
            'datos': self.datos,
        }
    
    def _asegurar_datos_atributos(self):
        if ATR_SELLABLE in self.atributos:
            self.datos['sellado'] = self.datos.get('sellado', False)
            self.datos['permisos_sellado'] = self.datos.get('permisos_sellado', [])
        if ATR_ESCLUSA in self.atributos:
            self.datos['modo_esclusa'] = self.datos.get('modo_esclusa', 'NULL')
            self.datos['permisos_esclusa'] = self.datos.get('permisos_esclusa', [])

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        out_sala = Sala('', 1)
        out_sala.id = fuente.get('id', 'ERR500__invalid_id')
        out_sala.nombre = fuente.get('nombre', 'ERR500__invalid_name')
        out_sala.descripcion = fuente.get('descripcion', 'ERR500__invalid_desc')
        out_sala.aforo = fuente.get('aforo', 1)
        out_sala.is_puerta_abierta = fuente.get('is_puerta_abierta', False)
        out_sala.estado = fuente.get('estado', 100)
        out_sala.permisos = fuente.get('permisos', [])
        out_sala.atributos = fuente.get('atributos', [])
        out_sala.datos = fuente.get('datos', out_sala.datos)
        out_sala._asegurar_datos_atributos()
        return out_sala


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
    combustible: Combustible = Combustible(100, 100, False)

    # Salas
    salas: list[Sala] = []

    # Suministros
    stocks: dict[str, Stock]= {}

    @staticmethod
    def from_dict(fuente: dict[str, any]):
        arca = Arca()
        arca.health = Health.from_dict(fuente.get('health', {}))
        stocks: dict[str, tuple[int, str]] = fuente.get('stocks', {})
        for stock, val in stocks.items():
            arca.stocks[stock] = Stock.from_tuple(val)
        arca.combustible = Combustible.from_dict(fuente.get('combustible', {}))
        salas: list[dict[str, any]] = fuente.get('salas', [])
        for sala in salas:
            arca.salas.append( Sala.from_dict(sala))
        
        return arca

    def to_dict(self):
        stocks = dict[str, dict[str, tuple[int, str]]]
        for stock, value in self.stocks.items():
            stocks[stock] = value.to_tuple()
        return {
            'health': self.health.to_dict(),
            'combustible': self.combustible.to_dict(),
            'stocks': stocks,
            'salas': list(map((lambda sala: sala.to_dict()), self.salas))
        }
