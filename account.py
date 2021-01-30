from util.settings import *


class Account:
    def __init__(self, name='Client', account_balance=0):
        self._name = name
        self._balance = account_balance
        self._transactions = {}

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

    def add_balance(self, amount):
        balance = int(self._balance)
        if balance + amount > get_max_balance():
            raise ValueError(f"Balance can't be higher than {get_max_balance()}. Balance after: {balance + amount}")
        else:
            self._balance += amount

    def sub_balance(self, amount):
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

    def add_transaction(self, transaction):
        self._transactions[f'{transaction.get_id()}'] = transaction

    def get_info(self):
        return dict(name=self._name, balance=self._balance, transactions=str(self._transactions.__len__()))


def get_max_balance():
    return app_settings.get_setting("max_balance")
