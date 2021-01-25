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
        if balance < 0:
        	print(f"Balance can't be lower than 0. value: {balance}")
        else:
        	self._balance = balance
    
    def subBalance(self, amount):
    	pass
    
    def addBalance(self, amount):
    	pass

    @property
    def transactions(self):
        return self._transactions

    @transactions.setter
    def transactions(self, transactions):
        self._transactions = transactions

    def getInfo(self):
        return dict(name=self._name, balance=self._balance, transactions=str(self._transactions.__len__()))
