import util.settings as settings


class Account:
    def __init__(self, name='Client', account_balance=0):
        self.id = settings.next_acc_id()
        self.name = name
        self.balance = account_balance

    def add_balance(self, amount):
        balance = int(self.balance)
        if balance + amount > settings.get_max_balance():
            raise ValueError(f"Balance can't be higher than {settings.get_max_balance()}. Balance after: {balance + amount}")
        else:
            self.balance += amount

    def sub_balance(self, amount):
        balance = int(self.balance)
        if balance - amount < 0:
            raise ValueError(f"Balance can't be below zero. Balance: {balance}")
        else:
            self.balance -= amount

    def get_info(self):
        return dict(name=self.name, balance=self.balance)
