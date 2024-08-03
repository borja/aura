from os import read
from os.path import isfile, basename
import glob

class Texts:
    path: str

    txt_ayuda: str = ""
    txt_leyes: str = ""
    txt_normas: str = ""
    txt_salas: str = ""
    txt_saludo: str = ""
    txt_tripulantes: str = ""
    txt_welcome: str = ""

    def __init__(self, path: str):
        self.path = path
        self.reload()

    def reload(self):
        files = glob.glob(f"{self.path}/**.md")
        for file in files:
            if isfile(file) is False:
                continue
            name = basename(file).replace(".md","")
            match name:
                case "ayuda":
                    self.txt_ayuda = open(file, mode="r", encoding="utf-8").read()
                case "leyes":
                    self.txt_leyes = open(file, mode="r", encoding="utf-8").read()
                case "normas":
                    self.txt_normas = open(file, mode="r", encoding="utf-8").read()
                case "salas":
                    self.txt_salas = open(file, mode="r", encoding="utf-8").read()
                case "saludo":
                    self.txt_saludo = open(file, mode="r", encoding="utf-8").read()
                case "tripulantes":
                    self.txt_tripulantes = open(file, mode="r", encoding="utf-8").read()
                case "welcome":
                    self.txt_welcome = open(file, mode="r", encoding="utf-8").read()
                case _:
                    pass