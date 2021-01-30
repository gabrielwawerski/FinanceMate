from util.serializer import SettingsSerializer


class Settings:
    def __init__(self):
        self.serializer = SettingsSerializer()
        self.settings = {}

    def get_setting(self, name):
        return self.settings[name]

    def set_setting(self, name, value):
        print(f"Setting {name} to {value}")
        self.settings[name] = value

    def save(self):
        self.serializer.save(self.settings)

    def load(self):
        self.settings = self.serializer.load()


app_settings = Settings()


class Util:
    @staticmethod
    def get_currency():
        return app_settings.get_setting("currency")

    @staticmethod
    def get_max_balance():
        return app_settings.get_setting("max_balance")