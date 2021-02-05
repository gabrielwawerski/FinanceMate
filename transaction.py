import platform
from enum import Enum
import util.settings as settings
from util.utils import timestamp


class TransactionType(Enum):
    ADD = 1
    PAY = 2


class Transaction:
    def __init__(self, uid, account, amount, transaction_type, name="Transaction name", description="Short transaction description"):
        self.id = uid
        self.transaction_type = transaction_type.value
        self.name = name
        self.description = description
        self.account_id = account.id
        self.amount = float(amount)
        _acc_bal = float(account.balance)
        self.balance_after = _acc_bal - self.amount if transaction_type is TransactionType.PAY else _acc_bal + self.amount
        self.timestamp = timestamp()
        self.platform = "Mobile" if platform.node() == "localhost" else platform.node()
        self.os = platform.platform()

        print(f"{account.name}'s Transaction no. {self.id}: {self.sign()}{amount}{settings.get_currency()}")

    def sign(self):
        return "-" if self.transaction_type is TransactionType.PAY.value else "+"

    def get_id(self):
        return self.id

    def get_info(self):
        print(f"{self.id}: {self.transaction_type}")
        print(f"Account: {self.account_id}\nAmount:{self.amount}{settings.get_currency()}\n{self.timestamp}")


class PayTransaction(Transaction):
    def __init__(self, uid, account, amount):
        super().__init__(uid, account, amount, TransactionType.PAY)


class AddTransaction(Transaction):
    def __init__(self, uid, account, amount):
        super().__init__(uid, account, amount, TransactionType.ADD)
