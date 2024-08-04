class Settings:
    bot_id: str

    def __init__(self, dict: dict[str, str]):
        self.bot_id = dict.get('bot_id', '@aura_rol_bot')