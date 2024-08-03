from os import read
from typing import Final
import json

from infra.Settings import Settings
from infra.Telegram import Telegram
from infra.Texts import Texts

if __name__ == '__main__':
    print(" 🤖 AURA's systems are loading")

    # Token management
    with open("token.secret", mode="r", encoding="utf-8") as token_file:
        TOKEN: Final = token_file.read()

    # Configuration settings
    with open("settings.json", mode="r", encoding="utf-8") as config_file:
        CONFIG_JSON: Final = config_file.read()
    settings = Settings(json.loads(CONFIG_JSON))

    # Load Markdown Texts
    texts = Texts("assets/texts")

    # Main Object
    tel = Telegram(TOKEN, settings, texts)
