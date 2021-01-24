from account import *
from util.serializer import *


class App:
    def __init__(self):
        self._accounts = {}
        self.loadData()
        self._run = True

    def run(self):
        print("introductions")
        selection = input("> ")
        while self._run:
            pass

    def newAccount(self, *args):
        account = Account(*args)
        self._accounts[account.name] = account

    def listAccounts(self):
        print(f"Accounts: {len(self._accounts)}")
        # print("------------------")
        for acc in self._accounts.values():
            print(f"{acc.name}\nBalance: {acc.balance}\nTransactions: {len(acc.transactions)}")
            print("------------------")

    def saveData(self):
        Serializer.save(self._accounts, DataType.ACCOUNTS)

    def loadData(self):
        self._accounts = Serializer.load(DataType.ACCOUNTS)
        if self._accounts is None:
            self._accounts = {}
    
    def quit(self):
    	self.saveData()
