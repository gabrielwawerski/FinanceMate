from datetime import datetime
from enum import Enum
import util.settings as settings
import platform


class TransactionType(Enum):
    ADD = 1
    PAY = 2


class Transaction:
    def __init__(self, account, amount, transaction_type, description="description"):
        self.id = settings.TransactionID()()
        self.transaction_type = transaction_type.value
        self.description = description
        self.account_id = account.id
        self.amount = amount
        self.balance_after = account.balance - amount if transaction_type is TransactionType.PAY else account.balance + amount
        self.timestamp = timestamp()
        self.platform = platform.node()

        print(f"{self.account_id}'s Transaction no. {self.id}: {self.sign()}{amount}{settings.get_currency()}")

    def sign(self):
        return "-" if self.transaction_type is TransactionType.PAY.value else "+"

    def get_id(self):
        return self.id

    def get_info(self):
        print(f"{self.id}: {self.transaction_type}")
        print(f"Account: {self.account_id}\nAmount:{self.amount}{settings.get_currency()}\n{self.timestamp}")


class PayTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.PAY)


class AddTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.ADD)


def timestamp():
    dt = datetime.now()
    hour, minute, second, day, month = _format_date_time(dt.hour, dt.minute, dt.second, dt.day, dt.month)
    return f"{hour}:{minute}:{second} {day}.{month}.{dt.year}"


def _format_date_time(*data):
    fdata = list()
    for d in data:
        if d <= 9:
            d = str(d)
            fdata.append(d.replace(d, f"0{d}"))  # if value is below 9, insert 0 for proper formatting.
        else:
            fdata.append(str(d))
    return tuple(fdata)