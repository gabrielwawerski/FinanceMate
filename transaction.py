from datetime import datetime
from enum import Enum
from account import *
from util.serializer import *


class TransactionType(Enum):
    PAY = 1
    ADD = 2


class IDGenerator:
    def __init__(self):
        self._id = 0
        # TODO: load unique id from 'settings.json' here

    def __call__(self, *args, **kwargs):
        self._id += 1
        return self._id


class Transaction:
    def __init__(self, account, amount, transaction_type):
        self.account_name = account.name
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = datetime.now()
        self._id_generator = IDGenerator()
        self.id = self._id_generator()
        print(f"{self.account_name}'s transaction {self.id}, for {amount}")

        if transaction_type is TransactionType.PAY:
            account.sub_balance(amount)
        elif transaction_type is TransactionType.ADD:
            account.add_balance(amount)

        print(f"Current balance: {account.balance}")
        account.add_transaction(self)

    def get_id(self):
        return self.id

    def get_info(self):
        print(f"{self.id}: {self.transaction_type}:\nAccount: {self.account_name}\nAmount:{self.amount}\n{self.timestamp}")


class PayTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.PAY)


class AddTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.ADD)
