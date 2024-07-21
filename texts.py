from typing import Final

BOT_USERNAME: Final = '@aura_rol_bot'

COMMAND_HELP: Final = "ayuda"
COMMAND_DO: Final = "haz"
COMMAND_SAY: Final = "dime"

WELCOME: Final = "Saludos. Estás entrando al sistema de asistente personal AURA. Esperemos que su estancia en el submarino ARCA sea agradable."
HELP_TEXT: Final = """Estas son las funciones que puedes realizar:
 - Ayuda: Muestra el texto de los comandos que puedes hacer en cada momento
 - Dime:
   - Estado: Informa del estado de salud actual del submarino
   - Inventario: Informa de la cantidad de comida almacenada
 - Haz:
   - Autodestruccion: Empieza la secuencia de autodestrucción del submarino, sentíamos que faltaba algo si no teníamos esta función.
   - Cancelamiento: Creemos en las segundas oportudinades. Esto aborta la autodestrucción del submarino.
Ejemplos:
`Dime estado`
`Dime inventario`
`Haz autodestrucción`
`Haz Cancelamiento`
"""