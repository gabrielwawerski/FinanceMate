import json
import jsonpickle
from json import JSONEncoder
from enum import Enum
from util.config import *


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
        data_type = self.data_type

        for dataType in DataType:
            if dataType is self.data_type:
                with open(self.file_name, "w") as file:
                    print(f"{self.data_type} saved.")
                    file.write(jsonpickle.encode(data))

    def load(self):
        print(f"Load {self.data_type}...", end=" ")
        data_type = self.data_type
        for dataType in DataType:
            if dataType is self.data_type:
                with open(self.file_name, "r") as file:
                    print("Done.")
                    data = jsonpickle.decode(file.read())
        return data


class SettingsSerializer(SimpleSerializer):
    def __init__(self):
        super().__init__(DataType.SETTINGS)


class AccountSerializer(SimpleSerializer):
    def __init__(self):
        super().__init__(DataType.ACCOUNTS)


class TransactionSerializer(SimpleSerializer):
    def __init__(self):
        super().__init__(DataType.TRANSACTIONS)
