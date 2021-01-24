from account import *
from util.serializer import *


class App:
    def __init__(self, account):
        self._accounts = {account.name: account}
        self._run = True

    def run(self):
        print("introductions")
        selection = input("> ")
        while self._run:
            pass

    def newAccount(self, accountName, balance):
        account = Account(accountName, balance)
        self._accounts.update(account.getInfo())

    def listAccounts(self):
        print("Accounts:")
        # print("------------------")
        for acc in self._accounts.values():
            print(f"{acc}")
            print("------------------")

    def saveData(self):
        self.saveAccountsData()

    def saveAccountsData(self):
        Serializer.save(self._accounts, DataType.ACCOUNTS)

    def loadData(self):
        self._accounts = Serializer.load(DataType.ACCOUNTS)


class SimpleApp:
    def __new__(cls, name='Gabe W', balance="0"):
        return App(Account(name, balance))

