server_url = "https://gabrielwawerski.github.io/FinanceMate/"
data_dir = "data/"
full_data_url = server_url + data_dir
default_settings = "settings_default.json"


ftp_hostname = ""
ftp_username = ""
ftp_password = ""


class Settings:
    def __init__(self):
        self.settings = {}

    def get_setting(self, name: str) -> str:
        print(f"getting {name}")
        return self.settings[name]

    def set_setting(self, setting: str, value: str or int):
        print(f"[Settings Change] {setting}: {self.get_setting(setting)} -> {value}")
        if setting in self.settings:
            self.settings[setting] = value
        else:
            print(f"No such setting: {setting}")

    def add_setting(self, setting: str, value: str or int):
        self.settings[setting] = value

    def _add_settings(self, **args: tuple):
        for k, v in args.items():
            self.settings[k] = v

    def __call__(self, *args, **kwargs) -> dict:
        return self.settings

    def load(self, settings: dict):
        self.settings = settings


app_settings = Settings()



