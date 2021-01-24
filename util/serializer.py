import json
import jsonpickle
from json import JSONEncoder
from enum import Enum
from util.config import *


class DataType(Enum):
    ACCOUNTS = 1


class Serializer:
    @staticmethod
    def save(data, dataType=DataType.ACCOUNTS):
        if dataType is DataType.ACCOUNTS:
            with open(ACCOUNTS_FIlE, "w") as file:
                file.write(jsonpickle.encode(data))

    @staticmethod
    def load(dataType):
        data = {}
        if dataType is DataType.ACCOUNTS:
            with open(ACCOUNTS_FIlE, "r") as file:
                data = jsonpickle.decode(file.read())
        return data
