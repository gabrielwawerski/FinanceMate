import ftplib
import util.settings as settings
import util.serializer as serializer
from account import Account
from transaction import AddTransaction, PayTransaction, TransactionType


ftp = ftplib.FTP(settings.ftp_host, settings.ftp_username, settings.ftp_password)


class Service:
    def __init__(self):
        self._accounts = {}
        self._transactions = {}
        self._settings = settings.app_settings

        self._settings_serializer = serializer.ServerSerializer("settings")
        self._acc_serializer = serializer.ServerSerializer("accounts")
        self._trans_serializer = serializer.ServerSerializer("transactions")

        self.load_data()
        self.currency = self.get_currency()

    def login(self):
        pass

    def new_transaction(self, acc, amount, transaction_type):
        with transaction(acc, amount, transaction_type) as trans:
            self._transactions[f'{trans.get_id()}'] = trans
        self.save_transactions()
        self.save_settings()

    def new_account(self, name, balance):
        with account(name, balance) as acc:
            self._accounts[acc.name] = acc
        self.save_accounts()
        self.save_settings()

    def addtrans(self, _account, amount):
        self.add_acc_bal(_account, amount)
        return AddTransaction(self.next_trans_id(), _account, amount)

    def paytrans(self, _account, amount):
        self.sub_acc_bal(_account, amount)
        return PayTransaction(self.next_trans_id(), _account, amount)

    def ftp_retr(self, path, filename, file):
        return ftp.retrbinary(f"RETR {path}/{filename}", file.write)

    def ftp_stor(self, path, filename):
        ftp.storbinary(f"STOR /{path}", filename)

    def add_acc_bal(self, _account, amount):
        _account.add_balance(amount)
        return self

    def sub_acc_bal(self, _account, amount):
        _account.sub_balance(amount)
        return self

    def next_acc_id(self):
        _acc_uid = self.get_acc_uid()
        settings.app_settings.set_setting("acc_uid", _acc_uid + 1)
        return _acc_uid

    def next_trans_id(self):
        _trans_uid = self.get_trans_uid()
        self._settings.set_setting("trans_uid", _trans_uid + 1)
        return int(_trans_uid)

    def set_default_settings(self):
        self._settings.load(self.from_server())

    def from_server(self):
        import requests
        import jsonpickle

        data = requests.get(f"{settings.full_data_url}{settings.default_settings}").text
        return dict(jsonpickle.decode(data))

    def transactions(self):
        return self._transactions

    def get_acc_transactions(self, acc):
        transactions = list()
        for t in self.transactions().values():
            if t.account_id == acc.id:
                transactions.append(t)
        return tuple(transactions)

    def accounts(self):
        return self._accounts

    def get_account(self, accountName):
        return self.accounts().get(accountName)

    def settings(self):
        return self._settings

    def get_acc_uid(self):
        return self._settings.get_setting("acc_uid")

    def get_trans_uid(self):
        return self._settings.get_setting("trans_uid")

    def get_currency(self):
        return self._settings.get_setting("currency")

    def get_max_balance(self):
        return self._settings.get_setting("max_balance")

    def get_timeout(self, ):
        return self._settings.get_setting("timeout")

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

    def load_settings(self):
        self._settings.load(self._settings_serializer.load())

    def load_transactions(self):
        self._transactions = self._trans_serializer.load()

    def load_accounts(self):
        self._accounts = self._acc_serializer.load()

    def load_data(self):
        self.load_settings()
        self.load_transactions()
        self.load_accounts()

        if self._settings is None:
            self._transactions = {}

        if self._transactions is None:
            self._transactions = {}

        if self._accounts is None:
            self._accounts = {}

    def quit(self):
        self.save_data()
        quit()


service = Service()


class account:
    def __init__(self, _name, balance):
        self.name = _name
        self.balance = balance

    def __enter__(self):
        return Account(service.next_acc_id(), self.name, self.balance)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class transaction:
    def __init__(self, _account, amount, transaction_type):
        self.account = _account
        self.amount = amount
        self.transaction_type = transaction_type

    def __enter__(self):
        if self.transaction_type == str(TransactionType.PAY) or self.transaction_type is TransactionType.PAY:
            return service.paytrans(self.account, self.amount)
        elif self.transaction_type == str(TransactionType.ADD) or self.transaction_type is TransactionType.ADD:
            return service.addtrans(self.account, self.amount)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
