from util.settings import *


class Account:
    def __init__(self, name='Client', account_balance=0):
        self.name = name
        self.balance = account_balance
        self.transactions = {}

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

    def add_transaction(self, transaction):
        self.transactions[f'{transaction.get_id()}'] = transaction

    def get_info(self):
        return dict(name=self.name, balance=self.balance, transactions=str(self.transactions.__len__()))
