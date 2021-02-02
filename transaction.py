from datetime import datetime
from enum import Enum
import util.settings as settings


class TransactionType(Enum):
    PAY = 1
    ADD = 2


class Transaction:
    def __init__(self, account, amount, transaction_type):
        self.id = settings.TransactionID()()
        self.account_name = account.name
        self.amount = amount
        self.transaction_type = transaction_type

        dt = datetime.now()
        hour, minute, second, day, month = format_time_date(dt.hour, dt.minute, dt.second, dt.day, dt.month)
        self.timestamp = f"{hour}:{minute}:{second} {day}.{month}.{dt.year}"

        print(f"{self.account_name}'s Transaction no. {self.id}: {self.sign()}{amount}{settings.get_currency()}")
        print(f"Current balance: {account.balance}{settings.get_currency()}")

    def sign(self):
        return "-" if self.transaction_type is TransactionType.PAY else TransactionType.ADD

    def get_id(self):
        return self.id

    def get_info(self):
        print(f"{self.id}: {self.transaction_type}")
        print(f"Account: {self.account_name}\nAmount:{self.amount}{settings.get_currency()}\n{self.timestamp}")


class PayTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.PAY)


class AddTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.ADD)


def format_time_date(*data):
    alist = list()
    for d in data:
        if d <= 9:
            d = str(d)
            alist.append(d.replace(d, f"0{d}"))  # if value is below 9, insert 0 for proper formatting.
        else:
            alist.append(str(d))
    return tuple(alist)
