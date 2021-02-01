import jsonpickle
from json import JSONEncoder
from enum import Enum
import json
import urllib.request

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


class SimpleSerializer(Serializer):
    def save(self, data):
        print(f"Saving {self.data_type}...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with open(path + self.file_name, "w") as file:
                    print("Done.")
                    file.write(jsonpickle.encode(data))

    def load(self):
        print(f"Loading {self.data_type}...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with open(path + self.file_name, "r") as file:
                    print("Done.")
                    return jsonpickle.decode(file.read())


class ServerSerializer(Serializer):
    def save(self, data):
        print(f"Saving {self.data_type}...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with open(path + self.file_name, "w") as file:
                    print("Done.")
                    file.write(jsonpickle.encode(data))

    def load(self):
        print(f"Loading {self.data_type}...", end=" ")
        server_url = "https://gabrielwawerski.github.io/FinanceMate/"
        for dataType in DataType:
            if dataType is self.data_type:
                with urllib.request.urlopen(f"{server_url}{self.data_type}") as url:
                    print(f"https://gabrielwawerski.github.io/FinanceMate/{self.data_type}")
                    data = url.read()
                    print("Done.")
                    return jsonpickle.decode(data)


class SettingsSerializer(SimpleSerializer):
    def __init__(self):
        super().__init__(DataType.SETTINGS)


class AccountSerializer(SimpleSerializer):
    def __init__(self):
        super().__init__(DataType.ACCOUNTS)


class TransactionSerializer(SimpleSerializer):
    def __init__(self):
        super().__init__(DataType.TRANSACTIONS)
