class Account:
    def __init__(self, uid: int, name: str = 'Client', account_balance: float = 0):
        self.id = uid
        self.name = name
        self.balance = "{:.2f}".format(account_balance)

    def add_balance(self, amount: float):
        val = float(self.balance) + float(amount)
        self.balance = "{:.2f}".format(val)

    def sub_balance(self, amount: float):
        val = float(self.balance) - float(amount)
        self.balance = "{:.2f}".format(val)
