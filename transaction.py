from datetime import datetime
from enum import Enum
from account import *
from util.serializer import *
from util.settings import *


class TransactionType(Enum):
    PAY = 1
    ADD = 2


class ID:
    def __init__(self):
        self.id = app_settings.get_setting("uid")
        # TODO: load unique id from 'settings.json' here

    def __call__(self, *args, **kwargs):
        self.id += 1
        app_settings.set_setting("uid", self.id)
        return self.id


class Transaction:
    def __init__(self, account, amount, transaction_type):
        self.account_name = account.name
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = datetime.now()
        self._id = ID()
        self.id = self._id()
        print(f"{self.account_name}'s Transaction no. {self.id} - for {amount}{CURRENCY}")

        if transaction_type is TransactionType.PAY:
            account.sub_balance(amount)
        elif transaction_type is TransactionType.ADD:
            account.add_balance(amount)

        print(f"Current balance: {account.balance}{CURRENCY}")
        account.add_transaction(self)

    def get_id(self):
        return self.id

    def get_info(self):
        print(f"{self.id}: {self.transaction_type}:\nAccount: {self.account_name}\nAmount:{self.amount}{CURRENCY}\n{self.timestamp}")


class PayTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.PAY)


class AddTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.ADD)
