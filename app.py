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
        self._accounts[account.name] = account

    def listAccounts(self):
        print("Accounts:")
        # print("------------------")
        for acc in self._accounts.values():
            print(f"{acc.name}\nBalance: {acc.balance}\nTransactions: {len(acc.transactions)}")
            print("------------------")

    def saveData(self):
        Serializer.save(self._accounts, DataType.ACCOUNTS)

    def loadData(self):
        self._accounts = Serializer.load(DataType.ACCOUNTS)


class SimpleApp:
    def __new__(cls, name='Gabe W', balance="0"):
        return App(Account(name, balance))

