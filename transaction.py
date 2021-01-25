from datetime import datetime
from enum import Enum
from account import *
from util.serializer import *


class TransactionType(Enum):
    PAY = 1
    ADD = 2


class Transaction:
    def __init__(self, account, amount, transactionType):
        self.account = account
        self.amount = amount
        self.transactionType = transactionType
        self.timestamp = datetime.now()

        if transactionType is TransactionType.PAY:
            account.subBalance(amount)
        elif transactionType is TransactionType.ADD:
            account.addBalance(amount)

        print(f"transaction: {self.amount}")
        account.addTransaction(self)


class PayTransaction(Transaction):
    def __init__(self, account, amount):
        super().__init__(account, amount, TransactionType.PAY)
        account.addTransaction(self)
