class Settings:
    bot_id: str
    save_method: str
    save_endpoint: str

    def __init__(self, dict: dict[str, str]):
        self.bot_id = dict.get("bot_id", "@aura_rol_bot")
        self.save_method = dict.get("save_method", "file")
        self.save_endpoint = dict.get("save_endpoint", "test.json")