class Health:
    is_arca_autodestructing: bool = False
    temperatura_interior: int = 23
    soporte_vital: int = 100
    cellar: int = 100
    reactor: int = 100
    exterior: int = 100
    circuits: int = 100
    boiler: int = 100
    gardens: int = 100
    sleeping_quarters: int = 100

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

class Arca:
    health: Health = Health()
    fuel: Combustible = Combustible(100, 100, False)
    stocks: dict[str, Stock]= {
        'algolosina': Stock(32, "u"),
    }
