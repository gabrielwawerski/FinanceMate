from functools import reduce

from transaction import *
from account import *
from util.settings import *


class MenuOption(Enum):
    ADD_TRANSACTION = 1
    ACCOUNT_INFO = 2
    LIST_TRANSACTIONS = 3
    LIST_ACCOUNTS = 4
    ADD_ACCOUNT = 5
    EXIT = 0

    def __str__(self):
        option = str.title((str(self.name)))
        return option.replace("_", " ")


# TODO: Account Viewer: class that holds one account at a time. Can perform operations on it (adding transactions etc.)
#       Helper class so App's methods dealing with accounts doesn't need individual accounts.
# TODO: move methods operating on accounts from here? to account viewer?
# TODO: json data from server (github pages)
# TODO: login
class App:
    """
    v0.2:
        - Fixed transaction serializing by adding new `settings` value in DataType enum
        - and adding `uid` (unique transaction id) to it
        - Added loading json data from (github pages) server

    v0.1:
        - Added Serializer class for easy data storing/loading to/from .json
        -


    """
    def __init__(self):
        self._transactions = {}
        self._accounts = {}
        self.settings = app_settings
        self._trans_serializer = TransactionSerializer()
        self._acc_serializer = AccountSerializer()
        self.version = "0.2"

        self.load_data()
        self._run = True

    def run(self):
        def print_menu():
            print("-" * 30)
            for option in MenuOption:
                print(f"{option.value}. {str(option)}")

        account = self.get_account('Gabriel Wawerski')

        print(f"FinanceMate v{self.version}")
        print_menu()
        selection = int(input("> "))
        while self._run:
            if selection is MenuOption.ADD_TRANSACTION.value:
                print("How much did you pay?")
                amount = int(input("> "))
                self.new_transaction(account, amount, TransactionType.PAY)
            elif selection is MenuOption.ACCOUNT_INFO.value:
                self.account_info(account)
            elif selection is MenuOption.LIST_TRANSACTIONS.value:
                self.list_transactions(account)
            elif selection is MenuOption.LIST_ACCOUNTS.value:
                self.list_accounts()
            elif selection is MenuOption.ADD_ACCOUNT.value:
                print("Create a new Account:")
                print("Account Name:", end=" ")
                acc_name = input("> ")
                print("Balance (default 0):", end=" ")
                acc_balance = input("> ")
                if acc_balance == "" or acc_balance == " ":
                    acc_balance = 0
                else:
                    acc_balance = int(acc_balance)

                self.new_account(acc_name, acc_balance)
            elif selection is MenuOption.EXIT.value:
                print("quit!")
                self.quit()
            else:
                print("else!")

            print_menu()
            selection = int(input("> "))

    def new_transaction(self, account, amount, transaction_type):
        if transaction_type is TransactionType.PAY:
            pay_trans = PayTransaction(account, amount)
            self._transactions[f"{pay_trans.get_id()}"] = pay_trans
            self.save_transactions()
            return pay_trans
        elif transaction_type is TransactionType.ADD:
            add_trans = AddTransaction(account, amount)
            self._transactions[f'{add_trans.get_id()}'] = add_trans
            self.save_transactions()
            return add_trans

    def get_account(self, accountName):
        """doc"""
        print(f"accounts: {self._accounts.keys()}")
        return self._accounts.get(accountName)

    def account_info(self, account):
        print("Account info:")
        print("-" * 30)
        print(f"{account.name}\nBalance: {account.balance}{get_currency()}\nTransactions: {len(self._get_acc_transactions(account))}")

    def list_transactions(self, account):
        print("-" * 30)
        print(f"{account.name}({account.balance}{get_currency()}) Transactions: ({len(self._get_acc_transactions(account))})")
        adict = self._transactions.values()
        for trans in adict:
            print(f"[{trans.get_id()}]. {trans.sign()}{trans.amount}{get_currency()}\n{trans.timestamp}")
            print("-" * 19)

    def list_accounts(self):
        print("-" * 30)
        print(f"Accounts: {len(self._accounts)}")
        print("-" * 30)
        for a in self._accounts.values():
            print(f"{a.name}\nBalance: {a.balance}{get_currency()}\nTransactions: {len(self._get_acc_transactions(a))}")
            print("-" * 19)

    def new_account(self, name, balance):
        account = Account(name, balance)
        self._accounts[account.name] = account
        print(f"Account: {account.name}, Balance: {account.balance}{get_currency()}")
        print("Account Created Succesfully.")
        self.save_accounts()

    def _get_acc_transactions(self, account):
        transactions = list()
        for t in self._transactions.values():
            if t.account_name == account.name:
                transactions.append(t)
        return tuple(transactions)

    @staticmethod
    def add_balance(account, amount):
        account.add_balance(amount)

    @staticmethod
    def sub_balance(account, amount):
        account.sub_balance(amount)

    def save_data(self):
        self.save_settings()
        self.save_transactions()
        self.save_accounts()

    def save_settings(self):
        self.settings.save()

    def save_accounts(self):
        self._acc_serializer.save(self._accounts)

    def save_transactions(self):
        self._trans_serializer.save(self._transactions)

    def load_data(self):
        self.settings.load()
        self._transactions = self._trans_serializer.load()
        self._accounts = self._acc_serializer.load()

        if self.settings is None:
            self._transactions = {}

        if self._transactions is None:
            self._transactions = {}

        if self._accounts is None:
            self._accounts = {}

    def quit(self):
        self.save_data()
        quit()
