from os.path import isfile, basename
import re
import glob

_vars_re = re.compile('{([a-z_]+)}', re.RegexFlag.IGNORECASE)

class Texts:
    path: str
    raws: dict[str, str] = {}

    def __init__(self, path: str):
        self.path = path
        self.reload()

    def reload(self):
        self.raws = {}
        files = glob.glob(f"{self.path}/**.html")
        for file in files:
            if isfile(file) is False:
                continue
            name = str.lower(basename(file).replace('.html',''))

            with open(file, mode='r', encoding='utf-8') as mango_archivo:
                self.raws[name] = mango_archivo.read()

    def build_text(self, nombre_texto: str, reemplazos: dict[str, str] = {}):
        fn = (lambda val: _replacer_fn(val, reemplazos))
        texto = self.raws.get(nombre_texto, f"ERR404_TEXT_{nombre_texto}_ERR404")
        return _vars_re.sub(fn, texto)

def _replacer_fn(val: re.Match[str], reemplazos: dict[str, str]):
    key = val.string[val.regs[1][0]:val.regs[1][1]]
    return str(reemplazos.get(key, f"ERR404_VAR_{val[1]}_ERR404"))
