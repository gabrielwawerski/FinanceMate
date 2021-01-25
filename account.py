from util.config import MAX_BALANCE


class Account:
    def __init__(self, name='Client', accountBalance=0):
        self._name = name
        self._balance = accountBalance
        print(type(self._balance))
        self._transactions = list()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        if int(balance) < 0:
            print(f"Balance can't be lower than 0. value: {balance}")
        else:
            self._balance = balance

    def addBalance(self, amount):
        balance = int(self._balance)
        if balance + amount > MAX_BALANCE:
            raise ValueError(f"Balance can't be higher than {MAX_BALANCE}. Balance after: {balance + amount}")
        else:
            self._balance += amount

    def subBalance(self, amount):
        balance = int(self._balance)
        if balance - amount < 0:
            raise ValueError(f"Balance can't be below zero. Balance: {balance}")
        else:
            self._balance -= amount

    @property
    def transactions(self):
        return self._transactions

    @transactions.setter
    def transactions(self, transactions):
        self._transactions = transactions

    def addTransaction(self, transaction):
        self._transactions.append(transaction)

    def getInfo(self):
        return dict(name=self._name, balance=self._balance, transactions=str(self._transactions.__len__()))
