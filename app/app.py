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
        option = str.capitalize((str(self.name)))
        return option.replace("_", " ")


# TODO: accomodate new "settings.json" file!
# TODO: unique transaction id - taken from new "settings.json" file
# TODO: remove self._transactions, store all transactions in account objects.
# TODO: fix displaying account transactions
# TODO: Account Viewer: class that holds one account at a time. Can perform operations on it (adding transactions etc.)
# Helper class so App's methods dealing with accounts doesn't need individual accounts.
# TODO: move methods operating on accounts from here? to account viewer? 
class App:
    def __init__(self):
        self._accounts = {}
        self._transactions = {}
        self.load_data()
        self._run = True

        self.version = "0.1"

    def run(self):
        def print_menu():
            print("-" * 30)
            for option in MenuOption:
                print(f"{option.value}. {str(option)}")

        account = self.get_account("Gabe")
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
            elif selection is MenuOption.ACCOUNT_TRANSACTIONS.value:
                self.list_account_transactions(account)
            elif selection is MenuOption.LIST_ACCOUNTS.value:
                self.list_accounts()
            elif selection is MenuOption.EXIT.value:
                print("exit!")
                self.quit()
            else:
                print("else!")

            print_menu()
            selection = int(input("> "))

    def new_transaction(self, account, amount, transaction_type):
        if transaction_type is TransactionType.PAY:
            pay_trans = PayTransaction(account, amount)
            self._accounts.get(account.name).add_transaction(pay_trans)
            self._transactions[f"{pay_trans.get_id()}"] = pay_trans
            return pay_trans
        elif transaction_type is TransactionType.ADD:
            add_trans = AddTransaction(account, amount)
            self._accounts.get(account.name).add_transaction(add_trans)
            self._transactions[f'{add_trans.get_id()}'] = add_trans
            return add_trans

    def get_account(self, accountName):
        """doc"""
        return self._accounts.get(accountName)

    def new_account(self, *args):
        account = Account(*args)
        self._accounts[account.name] = account

    def account_info(self, account):
        print("Account info:")
        print(f"{account.name}\nBalance: {account.balance}\nTransactions: {account.transactions}")

    def list_accounts(self):
        print(f"Accounts: {len(self._accounts)}")
        # print("------------------")
        for acc in self._accounts.values():
            print(f"{acc.name}\nBalance: {acc.balance}\nTransactions: {len(acc.transactions)}")
            print("------------------")

    def list_transactions(self):
        for t in self._transactions.values():
            print(f"{self._transactions[t]}. {t.amount}£\nAccount: {t.account_name}\n{t.timestamp}")

    def list_account_transactions(self, account):
        print(f"{account.name} transactions:")
        for t in account.transactions.values():
            print(f"{t.get_id()}. {t.amount}£\n{t.timestamp}")  # bug z id

    @staticmethod
    def add_balance(self, account, amount):
        account.add_balance(amount)

    @staticmethod
    def sub_balance(self, account, amount):
        account.sub_balance(amount)

    def save_data(self):
        AccountSerializer().save(self._accounts)
        TransactionSerializer().save(self._transactions)

    def load_data(self):
        self._transactions = TransactionSerializer().load()
        self._accounts = AccountSerializer().load()
        if self._accounts is None:
            self._accounts = {}

    def quit(self):
        self.save_data()
        quit()
