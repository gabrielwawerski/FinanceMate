import os
from enum import Enum
from pathlib import Path
from contextlib import closing
import jsonpickle
import urllib.request as request
import requests
import util.settings as settings

path = "data/"


# TODO: move up! (to data helper class?, make serializer generic?)
class DataType(Enum):
    ACCOUNTS = 1
    TRANSACTIONS = 2
    SETTINGS = 3

    def __str__(self, simple_name=False):
        if simple_name:
            return self.name.lower()
        else:
            return f"{self.name.lower()}.json"


class Serializer:
    def __init__(self, data_type):
        self.data_type = data_type
        self.file_name = str(data_type)

    def load(self):
        print(f"Loading {self.data_type}...", end=" ")
        if not isfile(path + self.file_name):
            print("File not found. Creating new file...", end=" ")
            # TODO: defaults for every file!!!
            with open(path + self.file_name, "r") as file:
                file.write("{}")
            print("Done.")
            return
        for dataType in DataType:
            if dataType is self.data_type:
                with open(path + self.file_name, "r") as file:
                    print("Done.")
                    return dict(jsonpickle.decode(file.read()))

    def save(self, data):
        print(f"Saving {self.data_type}...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with open(path + self.file_name, "w") as file:
                    print("Done.")
                    file.write(jsonpickle.encode(data))


class ServerSerializer(Serializer):
    def load(self):
        print(f"Loading {self.data_type}...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                data = requests.get(f"{settings.full_data_url}{self.data_type}").text
                if data is None or data == "{}":
                    settings.set_default_settings()
                    print("Done.")
                    return
                print("Done.")
                return dict(jsonpickle.decode(data))

    # def save(self, data):
    #     print(f"Saving {self.data_type}...", end=" ")
    #     for dataType in DataType:
    #         if dataType is self.data_type:
    #             r = requests.post(url, data)
    #             print("Done.")


serializer_type = Serializer


class SettingsSerializer(serializer_type):
    def __init__(self):
        super().__init__(DataType.SETTINGS)


class AccountSerializer(serializer_type):
    def __init__(self):
        super().__init__(DataType.ACCOUNTS)


class TransactionSerializer(serializer_type):
    def __init__(self):
        super().__init__(DataType.TRANSACTIONS)


def isfile(file_name):
    return os.path.isfile(file_name)


def mkfile(file_name):
    try:
        file_path = Path(path + file_name).resolve(strict=True)
    except FileNotFoundError:
        if not os.path.isfile(path + file_name):
            print(f"Loading default settings...")
            with open(path + file_name, "w+") as f:
                f.write(settings.server_default_settings())
    else:
        print(f"Already exists, omitting: {file_name}")
