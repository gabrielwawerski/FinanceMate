class Account:
    def __init__(self, name='Client', balance="0"):
        self._name = name
        self._balance = balance
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
        self._balance = balance

    @property
    def transactions(self):
        return self._transactions

    @transactions.setter
    def transactions(self, transactions):
        self._transactions = transactions

    def getInfo(self):
        return dict(name=self._name, balance=self._balance, transactions=str(self._transactions.__len__()))
