from account import *
from util.serializer import *
from transaction import *


class MenuOption(Enum):
    ADD_TRANSACTION = 1
    ACCOUNT_INFO = 2
    ACCOUNT_TRANSACTIONS = 3
    LIST_ACCOUNTS = 4
    EXIT = 0

    def __str__(self):
        returnValue = str.capitalize((str(self.name)))
        return returnValue.replace("_", " ")


# TODO: accomodate new "settings.json" file!
# TODO: unique transaction id - taken from new "settings.json" file
# TODO: remove self._transactions, store all transactions in account objects.
# TODO: fix displaying account transactions
# TODO: Account Viewer: class that holds one account at a time. Can perform operations on it (adding transactions etc.)
#       Helper class so App's methods dealing with accounts doesn't need individual accounts.
class App:
    def __init__(self):
        self._accounts = {}
        self._transactions = {}
        self.loadData()
        self._run = True

        self.version = "0.1"

    def run(self):
        def printMenu():
            print("-" * 30)
            for option in MenuOption:
                print(f"{option.value}. {str(option)}")

        account = self.getAccount("Gabe")
        print(f"FinanceMate v{self.version}")
        printMenu()
        selection = int(input("> "))

        while self._run:
            if selection == MenuOption.ADD_TRANSACTION.value:
                print("How much did you pay?")
                amount = int(input("> "))
                self.newTransaction(account, amount, TransactionType.PAY)
            elif selection == MenuOption.ACCOUNT_INFO.value:
                self.accountInfo(account)
            elif selection == MenuOption.ACCOUNT_TRANSACTIONS.value:
                self.listTransactions()
            elif selection == MenuOption.LIST_ACCOUNTS.value:
                self.listAccounts()
            elif selection == MenuOption.EXIT.value:
                print("exit!")
                self.quit()
            else:
                print("else!")

            printMenu()
            selection = int(input("> "))

    def newTransaction(self, account, amount, transactionType):
        if transactionType is TransactionType.PAY:
            payTrans = PayTransaction(account, amount)
            # self._accounts.get(account.name).addTransaction(payTrans)
            self._transactions[f"{payTrans.getID()}"] = payTrans
            return payTrans
        elif transactionType is TransactionType.ADD:
            addTrans = AddTransaction(account, amount)
            # self._accounts.get(account.name).addTransaction(addTrans)
            self._transactions[f'{addTrans.getID()}'] = addTrans
            return addTrans

    def getAccount(self, accountName):
        """doc"""
        return self._accounts.get(accountName)

    def newAccount(self, *args):
        account = Account(*args)
        self._accounts[account.name] = account

    def accountInfo(self, account):
        print("Account info:")
        print(f"{account.name}\nBalance: {account.balance}\nTransactions: {account.transactions}")

    def listAccounts(self):
        print(f"Accounts: {len(self._accounts)}")
        # print("------------------")
        for acc in self._accounts.values():
            print(f"{acc.name}\nBalance: {acc.balance}\nTransactions: {len(acc.transactions)}")
            print("------------------")

    def listTransactions(self):
        for t in self._transactions.values():
            print(f"{t.id.getLast()}. {t.amount}£\nAccount: {t.account.name}\n{t.timestamp}")

    def listAccountTransactions(self, account):
        print(f"{account.name} transactions:")
        for t in account.transactions.values():
            print(f"{t.id.getLast()}. {t.amount}£\n{t.timestamp}")  # bug z id

    @staticmethod
    def addBalance(self, account, amount):
        account.addBalance(amount)

    @staticmethod
    def subBalance(self, account, amount):
        account.subBalance(amount)

    def saveData(self):
        AccountSerializer().save(self._accounts)
        TransactionSerializer().save(self._transactions)

    def loadData(self):
        self._transactions = TransactionSerializer().load()
        self._accounts = AccountSerializer().load()
        if self._accounts is None:
            self._accounts = {}

    def quit(self):
        self.saveData()
        quit()
