from os import read
from typing import Final
import json

from infra.Settings import Settings
from infra.Telegram import Telegram

if __name__ == '__main__':
    print(" 🤖 AURA's systems are loading")

    # Token management
    token_file = open("token.secret", mode="r", encoding="utf-8")
    TOKEN: Final = token_file.read()
    token_file.close()
    # Config
    config_file = open("settings.json", mode="r", encoding="utf-8")
    configJson: Final = config_file.read()
    config_file.close()
    settingsDict = json.loads(configJson)
    settings = Settings(settingsDict)

    tel = Telegram(TOKEN, settings)

