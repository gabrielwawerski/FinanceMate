from account import *
from util.serializer import *
from transaction import *


class MenuOption(Enum):
    ADD_TRANSACTION = 1
    ACCOUNT_OVERVIEW = 2
    TRANSACTIONS = 3
    EXIT = 0


class App:
    def __init__(self):
        self._accounts = {}
        self._transactions = {}
        self.loadData()
        self._run = True

        self.version = "0.1"

    def run(self):
        def printMenu():
            print(f"{MenuOption.ADD_TRANSACTION.value}. Add Transaction")
            print(f"{MenuOption.ACCOUNT_OVERVIEW.value}. Account Info")
            print(f"{MenuOption.TRANSACTIONS.value}. Account Transactions")
            print(f"{MenuOption.EXIT.value}. Exit")

        print(f"FinanceMate v{self.version}")
        printMenu()
        selection = int(input("> "))
        account = self.getAccount("Gabe")
        # while selection != MenuOption.ADD_TRANSACTION.value or selection != MenuOption.ACCOUNT_OVERVIEW.value or selection != MenuOption.EXIT.value:
        #     print(f"Invalid option ({selection}). Relooping.")
        #     printMenu()
        #     selection = int(input())

        while self._run:
            if selection == MenuOption.ADD_TRANSACTION.value:
                print("add transaction!")
                print("How much did you pay?")
                amount = int(input("> "))
                PayTransaction(account, amount)
            elif selection == MenuOption.ACCOUNT_OVERVIEW.value:
                self.accountInfo(account)
            elif selection == MenuOption.TRANSACTIONS.value:
                self.listTransactions(account)
            elif selection == MenuOption.EXIT.value:
                print("exit!")
                quit()
            else:
                print("else!")
            printMenu()
            selection = int(input("> "))

    def getAccount(self, accountName):
        """doc"""
        return self._accounts.get(accountName)

    def newAccount(self, *args):
        account = Account(*args)
        self._accounts[account.name] = account

    def accountInfo(self, account):
        print("Account info:")
        print(f"{account.name}\nBalance: {account.balance}\nTransactions: {account.transactions}")

    def listTransactions(self, account):
        print(f"{account.name} transactions:")
        for x in account.transactions:
            print(f"Transaction value: {x.amount}")

    def listAccounts(self):
        print(f"Accounts: {len(self._accounts)}")
        # print("------------------")
        for acc in self._accounts.values():
            print(f"{acc.name}\nBalance: {acc.balance}\nTransactions: {len(acc.transactions)}")
            print("------------------")

    @staticmethod
    def addBalance(self, account, amount):
        account.addBalance(amount)

    @staticmethod
    def subBalance(self, account, amount):
        account.subBalance(amount)

    def saveData(self):
        AccountSerializer.save(self._accounts)
        TransactionSerializer.save()

    def loadData(self):
        TransactionSerializer.load()
        self._accounts = AccountSerializer.load()
        if self._accounts is None:
            self._accounts = {}

    def quit(self):
        self.saveData()
