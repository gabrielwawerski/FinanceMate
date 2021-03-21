import platform
from enum import Enum
import util.settings as settings
import app.service as service
from util.utils import timestamp


class TransactionType(Enum):
    ADD = 1
    PAY = 2

    def __str__(self):
        return self.name.lower()


class Transaction:
    def __init__(self, uid,
                 account,
                 amount,
                 transaction_type,
                 name="Transaction name",
                 description="Short transaction description"):
        self.id = uid
        self.transaction_type = transaction_type.value
        self.name = name
        self.description = description
        self.account_id = account.id
        self.amount = f"{amount:.2f}"

        _acc_bal, amt = float(account.balance), float(self.amount)
        self.balance_after = "{:.2f}".format(_acc_bal) if transaction_type is TransactionType.PAY else "{:.2f}".format(_acc_bal)

        self.sign = self._sign()
        self.platform = "Mobile" if platform.node() == "localhost" else platform.node()
        self.os = platform.platform()
        self.timestamp = timestamp()

        print(f"{account.name}'s Transaction no. {self.id}: {self._sign()}{amount}{service.service.get_currency()}")

    def _sign(self) -> str:
        return "-" if self.transaction_type is TransactionType.PAY.value else "+"

    def get_id(self) -> int:
        return self.id

    def get_info(self):
        print(f"{self.id}: {self.transaction_type}")
        print(f"Account: {self.account_id}\nAmount:{self.amount}{service.service.get_currency()}\n{self.timestamp}")


class PayTransaction(Transaction):
    def __init__(self, uid: int, account, amount: float):
        super().__init__(uid, account, amount, TransactionType.PAY)


class AddTransaction(Transaction):
    def __init__(self, uid: int, account, amount: float):
        super().__init__(uid, account, amount, TransactionType.ADD)
