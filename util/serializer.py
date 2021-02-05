import json
import os
from enum import Enum
from pathlib import Path
import jsonpickle
from app.service import ftp
import util.settings as settings


local_path = "data/"
server_path = "/htdocs/data/"


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
        self.path = local_path + self.file_name

    def load(self):
        print(f"Loading {self.data_type}...", end=" ")
        if not isfile(self.path):
            print("File not found. Creating new file...", end=" ")
            # TODO: defaults for every file!!!
            with open(self.path, "r") as file:
                file.write("{}")
            print("Done.")
            return
        for dataType in DataType:
            if dataType is self.data_type:
                with open(self.path, "r") as file:
                    print("Done.")
                    return dict(jsonpickle.decode(file.read()))

    def save(self, data):
        print(f"Saving {self.data_type}...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with open(self.path, "w") as file:
                    print("Done.")
                    file.write(jsonpickle.encode(data))


class ServerSerializer(Serializer):
    def load(self):
        print(f"Fetching {self.data_type} ({settings.ftp_host})... ", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with open(f"data/{self.file_name}", "wb") as server_file:
                    ftp.retrbinary(f"RETR {local_path}{self.file_name}", server_file.write)
                    # if data is None or data == "{}":
                    #     settings.set_default_settings()
                    #     print("Done.")
                    #     return
                print("Done.")
                with open(f"data/{self.file_name}", "rb") as file:
                    return dict(jsonpickle.decode(file.read()))

    def save(self, data):
        print(f"Uploading {self.data_type} ({settings.ftp_host})...", end=" ")
        for dataType in DataType:
            if dataType is self.data_type:
                with open(f"data/{self.file_name}", "w") as local_file:
                    local_file.write(jsonpickle.encode(data))
                    print("Done.")

                with open(f"data/{self.file_name}", "rb") as server_file:
                    ftp.storbinary(f"STOR htdocs/data/{self.file_name}", server_file)


def json_loads(data):
    return json.load(data)


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
        file_path = Path(local_path + file_name).resolve(strict=True)
    except FileNotFoundError:
        if not os.path.isfile(local_path + file_name):
            print(f"Loading default settings...")
            with open(local_path + file_name, "w+") as f:
                f.write(settings.from_server())
    else:
        print(f"Already exists, omitting: {file_name}")


def wipe_transactions():
    with open(local_path + "transactions.json", "w") as f:
        f.write("{}")
