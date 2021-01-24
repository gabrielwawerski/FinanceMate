from datetime import datetime
from enum import Enum
from account import *


class TransactionType(Enum):
    PAY = 1
    ADD = 2


class Transaction:
    def __init__(self, account, amount, trans_type):
        self.timestamp = datetime.now()
