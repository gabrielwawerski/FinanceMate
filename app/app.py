from enum import Enum

import app.service
import util.settings as settings
import util.serializer as serializer
from util.utils import fname as fnum
from account import Account
from transaction import PayTransaction, AddTransaction, TransactionType


class MenuEnum(Enum):
    def __str__(self):
        enum_entry = str.title((str(self.name)))
        return enum_entry.replace("_", " ")


class MainMenu(MenuEnum):
    ADD_TRANSACTION = 1
    ADD_BALANCE = 2
    ACCOUNT_INFO = 3
    LIST_TRANSACTIONS = 4
    LIST_ACCOUNTS = 5
    ADD_ACCOUNT = 6
    DEFAULT_SETTINGS = 7
    EXIT = 0


class Login(MenuEnum):
    pass


def inpt():
    return input("> ")


def finpt():
    return float(inpt())


# TODO: Account Viewer: class that holds one account at a time. Can perform operations on it (adding transactions etc.)
#       Helper class so App's methods dealing with accounts doesn't need individual accounts.
# TODO: move methods operating on accounts from here? to account viewer?
# TODO: login
# TODO: admin panel
    # TODO: remove account
class App:
    """
    v0.3:
        - Data is now stored on a server
        - Getting and sending data to server

    v0.2.1:
        - Simplified account data serializing
        - Data is now saved after operations on it
        - Fixed transaction data formatting

    v0.2:
        - Fixed transaction serializing by adding new `settings` value in DataType enum
        - and adding `uid` (unique transaction id) to it
        - Added loading json data from (github pages) server

    v0.1:
        - Added Serializer class for easy data storing/loading to/from .json
    """
    def __init__(self):
        # todo: move settings, data handling to service.py? i think
        self._settings = settings.app_settings
        self._accounts = {}
        self._transactions = {}
        self._settings_serializer = serializer.SettingsSerializer()
        self._acc_serializer = serializer.AccountSerializer()
        self._trans_serializer = serializer.TransactionSerializer()
        self.version = "0.3"

        self.load_data()

        self.currency = settings.get_currency()
        self._run = True

    def login(self):
        pass

    def run(self):
        def print_main_menu():
            div()
            for option in MainMenu:
                print(f"{option.value}. {str(option)}")

        account = self.get_account('Gabriel Wawerski')
        print(f"FinanceMate v{self.version}")
        print_main_menu()
        selection = int(inpt())

        while self._run:
            if selection is MainMenu.ADD_TRANSACTION.value:
                print("How much did you pay?")
                amount = finpt()
                self.new_transaction(account, amount, TransactionType.PAY)

            elif selection is MainMenu.ADD_BALANCE.value:
                print("How much did you deposit?")
                amount = finpt()
                self.new_transaction(account, amount, TransactionType.ADD)

            elif selection is MainMenu.ACCOUNT_INFO.value:
                self.account_info(account)

            elif selection is MainMenu.LIST_TRANSACTIONS.value:
                self.list_transactions(account)

            elif selection is MainMenu.LIST_ACCOUNTS.value:
                self.list_accounts()

            elif selection is MainMenu.ADD_ACCOUNT.value:
                print("Create a new Account:")
                print("Account Name:", end=" ")
                acc_name = inpt()
                print("Balance (default 0):", end=" ")
                acc_balance = inpt()
                if acc_balance == "" or acc_balance == " ":
                    acc_balance = 0
                self.new_account(acc_name, acc_balance)

            elif selection is MainMenu.DEFAULT_SETTINGS.value:
                settings.set_default_settings()
                self.save_settings()

            elif selection is MainMenu.EXIT.value:
                self.quit()

            else:
                print("else!")

            print_main_menu()
            selection = int(input("> "))

    def new_transaction(self, account, amount, transaction_type):
        if transaction_type is TransactionType.PAY:
            trans = PayTransaction(settings.get_trans_uid(), account, amount)
            self._sub_acc_bal(account, amount)
            self._add_transaction(trans)
            print(f"Current balance: {fnum(account.balance)}{self.currency}")

        elif transaction_type is TransactionType.ADD:
            add_trans = AddTransaction(settings.get_trans_uid(), account, amount)
            self._add_acc_bal(account, amount)
            self._add_transaction(add_trans)
            print(f"Current balance: {fnum(account.balance)}{self.currency}")

    def _add_transaction(self, transaction):
        self._transactions[f'{transaction.get_id()}'] = transaction  # add new transaction to db
        self.save_transactions()
        self.save_settings()

    def get_account(self, accountName):
        return self._accounts.get(accountName)

    def account_info(self, account):
        title("Account info:")
        print(f"{account.name}")
        print(f"Balance: {fnum(account.balance)}{self.currency}")
        print(f"Transactions: {len(self._get_acc_transactions(account))}")

    def list_transactions(self, account):
        title(f"{account.name}({account.balance}{self.currency})\nTransactions: {len(self._get_acc_transactions(account))}", 45)
        transactions = self._transactions.values()
        t_listing = 1
        # todo: move?
        for t in transactions:
            trans_amout = t.sign() + fnum(t.amount) + self.currency
            print(f"{t.name} {t_listing:>13}")
            t_listing += 1
            print(f"{trans_amout.rjust(30)}")
            print(t.description)
            print(f"Balance: {fnum(t.balance_after) + self.currency:>21}")
            print(f"Device: {t.platform.rjust(22)}")
            print(f"OS: {t.os.rjust(26)}")
            print(f"{t.timestamp}")
            div()

    def list_accounts(self):
        title(f"Accounts: {len(self._accounts)}")
        for a in self._accounts.values():
            print(f"{a.name}\nBalance: {fnum(a.balance)}{self.currency}")
            print(f"Transactions: {len(self._get_acc_transactions(a))}")
            subdiv()

    def new_account(self, name, balance):
        account = Account(settings.next_acc_id(), name, balance)
        self._accounts[account.name] = account
        print(f"Account: {account.name}, Balance: {fnum(account.balance)}{self.currency}")
        print("Account Created Succesfully.")
        self.save_accounts()
        self.save_settings()

    def _get_acc_transactions(self, account):
        transactions = list()
        for t in self._transactions.values():
            if t.account_id == account.id:
                transactions.append(t)
        return tuple(transactions)

    @staticmethod
    def _add_acc_bal(account, amount):
        account.add_balance(amount)

    @staticmethod
    def _sub_acc_bal(account, amount):
        account.sub_balance(amount)

    def save_data(self):
        self.save_settings()
        self.save_transactions()
        self.save_accounts()

    def save_settings(self):
        self._settings_serializer.save(self._settings())

    def save_accounts(self):
        self._acc_serializer.save(self._accounts)

    def save_transactions(self):
        self._trans_serializer.save(self._transactions)

    def load_data(self):
        self._settings.load(self._settings_serializer.load())
        self._transactions = self._trans_serializer.load()
        self._accounts = self._acc_serializer.load()

        if self._settings is None:
            self._transactions = {}

        if self._transactions is None:
            self._transactions = {}

        if self._accounts is None:
            self._accounts = {}

    def quit(self):
        self.save_data()
        quit()


def divider(length):
    print("-" * length)


def div():
    divider(30)


def subdiv():
    divider(19)


def title(atitle, length=30):
    divider(length)
    print(atitle)
    divider(length)
