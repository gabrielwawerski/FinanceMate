import os
from enum import Enum
from pathlib import Path
import jsonpickle
import urllib.request
from app.service import server_default_settings
from util.settings import default_settings, server_url

path = "data/"


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

    def save(self, data):
        print(f"Saving {self.data_type}...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with open(path + self.file_name, "w") as file:
                    print("Done.")
                    file.write(jsonpickle.encode(data))

    def load(self):
        print(f"Loading {self.data_type}...", end=" ")
        if not isfile(path + self.file_name):
            print("Done.")
            # TODO: defaults for every file!!!
            return default_settings()
        for dataType in DataType:
            if dataType is self.data_type:
                with open(path + self.file_name, "r") as file:
                    print("Done.")
                    return jsonpickle.decode(file.read())


class ServerSerializer(Serializer):
    def save(self, data):
        print(f"Saving {self.data_type}...", end=" ")
        full_path = path + self.file_name
        if not isfile(full_path):
            print("Done.")
            return default_settings()
        for dataType in DataType:
            if dataType is self.data_type:
                with open(path + self.file_name, "w") as file:
                    print("Done.")
                    file.write(jsonpickle.encode(data))

    def load(self):
        print(f"Loading {self.data_type}...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with urllib.request.urlopen(f"{server_url}{self.data_type}") as url:
                    data = url.read()
                    print("Done.")
                    return jsonpickle.decode(data)


class SettingsSerializer(Serializer):
    def __init__(self):
        super().__init__(DataType.SETTINGS)


class AccountSerializer(Serializer):
    def __init__(self):
        super().__init__(DataType.ACCOUNTS)


class TransactionSerializer(Serializer):
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
                f.write(server_default_settings())
    else:
        print(f"Already exists, omitting: {file_name}")
