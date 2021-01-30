from util.settings import *


class Account:
    def __init__(self, name='Client', account_balance=0):
        self.name = name
        self.balance = account_balance
        self.transactions = {}

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def balance(self):
        return self.balance

    @balance.setter
    def balance(self, balance):
        if int(balance) < 0:
            print(f"Balance can't be lower than 0. value: {balance}")
        else:
            self.balance = balance

    def add_balance(self, amount):
        balance = int(self.balance)
        if balance + amount > Util.get_max_balance():
            raise ValueError(f"Balance can't be higher than {Util.get_max_balance()}. Balance after: {balance + amount}")
        else:
            self.balance += amount

    def sub_balance(self, amount):
        balance = int(self.balance)
        if balance - amount < 0:
            raise ValueError(f"Balance can't be below zero. Balance: {balance}")
        else:
            self.balance -= amount

    @property
    def transactions(self):
        return self.transactions

    @transactions.setter
    def transactions(self, transactions):
        self.transactions = transactions

    def add_transaction(self, transaction):
        self.transactions[f'{transaction.get_id()}'] = transaction

    def get_info(self):
        return dict(name=self.name, balance=self.balance, transactions=str(self.transactions.__len__()))
