server_url = "https://gabrielwawerski.github.io/FinanceMate/"
data_dir = "data/"
full_data_url = server_url + data_dir
default_settings = "settings_default.json"
full_data_url = server_url + data_dir


class Settings:
    def __init__(self):
        self.settings = {}

    def get_setting(self, name):
        return self.settings[name]

    def set_setting(self, setting, value):
        print(f"[Settings Change] {setting}: {self.get_setting(setting)} -> {value}")
        if setting in self.settings:
            self.settings[setting] = value
        else:
            print(f"No such setting: {setting}")

    def add_setting(self, setting, value):
        self.settings[setting] = value

    def _add_settings(self, **args):
        for k, v in args.items():
            self.settings[k] = v

    def __call__(self, *args, **kwargs):
        return self.settings

    def load(self, settings):
        self.settings = settings


app_settings = Settings()


def next_acc_id():
    _acc_uid = get_acc_uid()
    app_settings.set_setting("acc_uid", _acc_uid + 1)
    return _acc_uid


def next_trans_id():
    _trans_uid = get_trans_uid()
    app_settings.set_setting("trans_uid", _trans_uid + 1)
    return int(_trans_uid)


def set_default_settings():
    app_settings.load(from_server())


def from_server():
    import requests
    import jsonpickle

    data = requests.get(f"{full_data_url}{default_settings}").text
    return dict(jsonpickle.decode(data))


def get_acc_uid():
    return app_settings.get_setting("acc_uid")


def get_trans_uid():
    return app_settings.get_setting("trans_uid")


def get_currency():
    return app_settings.get_setting("currency")


def get_max_balance():
    return app_settings.get_setting("max_balance")


def get_timeout():
    return app_settings.get_setting("timeout")
