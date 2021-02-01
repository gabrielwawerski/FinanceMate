from datetime import datetime
from util.serializer import *
from util.settings import *


class TransactionType(Enum):
    PAY = 1
    ADD = 2


def format_time_date(*data)
	for d in data:
		if d <= 9:
        	d = d.replace(d, f"0{str_day}")
        else:
            d
    return data

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


class Transaction:
    def __init__(self, account, amount, transaction_type):
        self.account_name = account.name
        self.amount = amount
        self.transaction_type = transaction_type
        dt = datetime.now()
        if dt.day <= 9:
            str_day = str(dt.day)
            day = str_day.replace(str_day, f"0{str_day}")
        else:
            day = dt.day

        if dt.month <= 9:
            str_month = str(dt.month)
            month = str_month.replace(str_month, f"0{str_month}")
        else:
            month = dt.month
        self.timestamp = f"{dt.hour}:{dt.minute}:{dt.second} {day}.{month}.{dt.year}"
        self.id = ID()()
        print(f"{self.account_name}'s Transaction no. {self.id} - for {amount}{Util.get_currency()}")

        if transaction_type is TransactionType.PAY:
            account.sub_balance(amount)
        elif transaction_type is TransactionType.ADD:
            account.add_balance(amount)

        print(f"Current balance: {account.balance}{Util.get_currency()}")

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
