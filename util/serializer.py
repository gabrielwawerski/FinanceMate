import json
import jsonpickle
from json import JSONEncoder
from enum import Enum
from util.config import *


class DataType(Enum):
    ACCOUNTS = 1
    TRANSACTIONS = 2


class Serializer:
    def __init__(self, dataType):
    	self.dataType = dataType

    def save(self, data):
        dataType = self.dataType
        if dataType is DataType.ACCOUNTS:
            with open(ACCOUNTS_FIlE, "w") as file:
                file.write(jsonpickle.encode(data))
        elif dataType is DataType.TRANSACTIONS:
            with open(TRANSACTIONS_FILE, "w") as file:
                file.write(jsonpickle.encode(data))
        else:  # if dataType is not of DataType, it's meaning changes to file name
            with open(dataType, "w") as file:
                file.write(data)

    def load(self):
        data = {}
        dataType = self.dataType
        if dataType is DataType.ACCOUNTS:
            with open(ACCOUNTS_FIlE, "r") as file:
                data = jsonpickle.decode(file.read())
        elif dataType is DataType.TRANSACTIONS:
            with open(TRANSACTIONS_FILE, "r") as file:
                data = jsonpickle.decode(file.read())
        else:  # if dataType is not of DataType, it's meaning changes to file name
            with open(dataType, "r") as file:
                data = jsonpickle.decode(file.read())
        return data


class AccountSerializer(Serializer):
    def __init__(self):
        super().__init__(self, DataType.ACCOUNTS)


class TransactionSerializer(Serializer):
    def __init__(self):
        super().__init__(self, DataType.TRANSACTIONS)
