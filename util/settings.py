from enum import Enum


# default settings

acc_uid = {"acc_uid": 0}
trans_uid = {"trans_uid": 0}
currency = {"currency": "Â£"}
max_balance = {"max_balance": 9999999999999999}
timeout = {"timeout": 10}


server_url = "https://gabrielwawerski.github.io/FinanceMate/"
data_dir = "data/"
default_settings = "settings_default.json"


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

    def _add_setting(self, **args):
        for k, v in args.items():
            self.settings[k] = v

    def get(self):
        return self.settings

    def load(self, settings):
        self.settings = settings


app_settings = Settings()


def default_settings():
    app_settings._add_setting(**acc_uid)
    app_settings._add_setting(**trans_uid)
    app_settings._add_setting(**currency)
    app_settings._add_setting(**max_balance)
    app_settings._add_setting(**timeout)
    return app_settings.get()


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


class IdType(Enum):
    ACC_UID = 0
    TRANS_UID = 1

    def __str__(self):
        print(self.name.lower())
        return self.name.lower()


class ID:
    def __init__(self, id_type):
        self.id_type = str(id_type)

    def __call__(self, *args, **kwargs):
        uid = app_settings.get_setting(self.id_type)
        app_settings.set_setting(self.id_type, uid + 1)
        return uid


class AccountID(ID):
    def __init__(self):
        super(AccountID, self).__init__(IdType.ACC_UID)


class TransactionID(ID):
    def __init__(self):
        super(TransactionID, self).__init__(IdType.TRANS_UID)
