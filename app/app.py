from enum import Enum
import app.service as service
from util.utils import fnum


# TODO: Account Viewer that holds one account at a time. Can perform operations on it (adding transactions etc.)
#       Helper class so App's methods dealing with accounts doesn't need individual accounts.
# TODO: move methods operating on accounts from here? to account viewer?
# TODO: login
# TODO: admin panel
# TODO: remove account
class App:
    """
    v1.0
        - Add function annotations
        - Cleanup, minor fixes
        - Add ftp module

    v0.3.2:
        - First attempt at loosening module coupling (imports)
        - Add service module, move logic there
        - Simplify and improve serializer, settings, accounts modules

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
        self.service = service.service
        self.version = "1.0"
        self._run = True
        self.currency = self.service.currency

    def run(self):
        def print_main_menu():
            div()
            for option in MainMenu:
                print(f"{option.value}. {str(option)}")

        account = self.service.get_account('Gabriel Wawerski')
        print(f"FinanceMate v{self.version}")
        print_main_menu()
        selection = int(inpt())
        _service = self.service

        while self._run:
            if selection is MainMenu.ADD_TRANSACTION.value:
                print("How much did you pay?")
                amount = finpt()
                _service.new_transaction(account, amount, "pay")
                print(f"Current balance: {fnum(account.balance)}{self.currency}")

            elif selection is MainMenu.ADD_BALANCE.value:
                print("How much did you deposit?")
                amount = finpt()
                _service.new_transaction(account, amount, "add")

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
                else:
                    acc_balance = float(acc_balance)
                _service.new_account(acc_name, acc_balance)
                print(f"Account: {acc_name}, Balance: {fnum(acc_balance)}{self.currency} Created succesfully.")

            elif selection is MainMenu.DEFAULT_SETTINGS.value:
                _service.set_default_settings()
                _service.save_settings()

            elif selection is MainMenu.EXIT.value:
                _service.quit()

            else:
                print("else!")

            print_main_menu()
            selection = int(input("> "))

    def account_info(self, account):
        title("Account info:")
        print(f"{account.name}")
        print(f"Balance: {fnum(account.balance)}{self.currency}")
        print(f"Transactions: {len(self.service.get_acc_transactions(account))}")

    def list_transactions(self, account):
        title(
            f"{account.name}({account.balance}{self.currency})\nTransactions: {len(self.service.get_acc_transactions(account))}",
            45)
        transactions = self.service.transactions().values()
        t_listing = 1
        # todo: move?
        for t in transactions:
            trans_amout = t.sign + fnum(t.amount) + self.currency
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
        title(f"Accounts: {len(self.service.accounts())}")
        for a in self.service.accounts().values():
            print(f"{a.name}\nBalance: {fnum(a.balance)}{self.currency}")
            print(f"Transactions: {len(self.service.get_acc_transactions(a))}")
            subdiv()


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


def divider(length):
    print("-" * length)


def div():
    divider(30)


def subdiv():
    divider(19)


def title(atitle: str, length: int = 30):
    divider(length)
    print(atitle)
    divider(length)


def inpt():
    return input("> ")


def finpt():
    return float(inpt())
