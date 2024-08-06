from os.path import isfile, basename
import glob

class Texts:
    path: str

    txt_ayuda: str = ''
    txt_leyes: str = ''
    txt_normas: str = ''
    txt_salas: str = ''
    txt_saludo: str = ''
    txt_tripulantes: str = ''
    txt_welcome: str = ''
    txt_scan: str = ''

    def __init__(self, path: str):
        self.path = path
        self.reload()

    def reload(self):
        files = glob.glob(f"{self.path}/**.md")
        for file in files:
            if isfile(file) is False:
                continue
            name = basename(file).replace('.md','')

            with open(file, mode='r', encoding='utf-8') as texto_interno:
                # Command selector:
                match name:
                    case 'ayuda':
                        self.txt_ayuda = texto_interno.read()
                    case 'leyes':
                        self.txt_leyes = texto_interno.read()
                    case 'normas':
                        self.txt_normas = texto_interno.read()
                    case 'salas':
                        self.txt_salas = texto_interno.read()
                    case 'saludo':
                        self.txt_saludo = texto_interno.read()
                    case 'tripulantes':
                        self.txt_tripulantes = texto_interno.read()
                    case 'welcome':
                        self.txt_welcome = texto_interno.read()
                    case 'scan':
                        self.txt_scan = texto_interno.read()
                    case _:
                        pass
