from datetime import datetime
from enum import Enum
from account import *
from util.serializer import *


class TransactionType(Enum):
    PAY = 1
    ADD = 2


class ID:
    def __init__(self):
        self._counter = 0

    def __call__(self, *args, **kwargs):
        self._counter += 1
        return self._counter

    def getLast(self):
        return self._counter


class Transaction:

    def __init__(self, account, amount, transactionType):
        self.account = account
        self.amount = amount
        self.transactionType = transactionType
        self.timestamp = datetime.now()
        self.id = ID()
        self._id = self.id()
        print(f"{account.name}'s transaction {self.id()}, for {amount}")

        if transactionType is TransactionType.PAY:
            account.subBalance(amount)
        elif transactionType is TransactionType.ADD:
            account.addBalance(amount)

        print(f"Current balance: {account.balance}")
        account.addTransaction(self)

    def getID(self):
        return self._id

    def getInfo(self):
        print(f"{self.id.getLast()}: {self.transactionType}:\nAccount: {self.account}\nAmount:{self.amount}\n{self.timestamp}")


class PayTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.PAY)


class AddTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.ADD)
