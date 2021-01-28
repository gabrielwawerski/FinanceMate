import json
import jsonpickle
from json import JSONEncoder
from enum import Enum
from util.config import *


class DataType(Enum):
    ACCOUNTS = 1
    TRANSACTIONS = 2


class Serializer:
    def __init__(self, data_type):
        self.data_type = data_type

    def save(self, data):
        data_type = self.data_type
        if data_type is DataType.ACCOUNTS:
            with open(ACCOUNTS_FIlE, "w") as file:
                file.write(jsonpickle.encode(data))
        elif data_type is DataType.TRANSACTIONS:
            with open(TRANSACTIONS_FILE, "w") as file:
                file.write(jsonpickle.encode(data))

    def load(self):
        data = {}
        data_type = self.data_type
        if data_type is DataType.ACCOUNTS:
            with open(ACCOUNTS_FIlE, "r") as file:
                data = jsonpickle.decode(file.read())
        elif data_type is DataType.TRANSACTIONS:
            with open(TRANSACTIONS_FILE, "r") as file:
                data = jsonpickle.decode(file.read())
        return data


class AccountSerializer(Serializer):
    def __init__(self):
        super().__init__(DataType.ACCOUNTS)


class TransactionSerializer(Serializer):
    def __init__(self):
        super().__init__(DataType.TRANSACTIONS)
