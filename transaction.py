from datetime import datetime
from util.serializer import *
from util.settings import *


class ID:
    def __init__(self):
        self.id = app_settings.get_setting("uid")
        # TODO: load unique id from 'settings.json' here

    def __call__(self, *args, **kwargs):
        self.id += 1
        app_settings.set_setting("uid", self.id)
        return self.id

    def __setstate__(self, state):
        state.setdefault('NodeText', None)

        for k, v in state.items():
            setattr(self, k, v)

    def __getstate__(self):
        state = self.__dict__.copy()

        del state['NodeText']
        return state

    def __repr__(self) -> str:
        return str(self.__dict__)


class TransactionType(Enum):
    PAY = 1
    ADD = 2


class Transaction:
    def __init__(self, account, amount, transaction_type):
        self.account_name = account.name
        self.amount = amount
        self.transaction_type = transaction_type
        self.id = ID()()

        dt = datetime.now()
        hour, minute, second, day, month = format_time_date(dt.hour, dt.minute, dt.second, dt.day, dt.month)
        self.timestamp = f"{hour}:{minute}:{second} {day}.{month}.{dt.year}"

        if transaction_type is TransactionType.PAY:
            account.sub_balance(amount)
        elif transaction_type is TransactionType.ADD:
            account.add_balance(amount)

        print(f"{self.account_name}'s Transaction no. {self.id}: {self.sign()}{amount}{Util.get_currency()}")
        print(f"Current balance: {account.balance}{Util.get_currency()}")

    def sign(self):
        if self.transaction_type is TransactionType.PAY:
            return "-"
        elif self.transaction_type is TransactionType.ADD:
            return "+"

    def get_id(self):
        return self.id

    def get_info(self):
        print(f"{self.id}: {self.transaction_type}")
        print(f"Account: {self.account_name}\nAmount:{self.amount}{Util.get_currency()}\n{self.timestamp}")


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
            d = d.replace(d, f"0{d}")
            alist.append(d)
        else:
            alist.append(str(d))
    return tuple(alist)
