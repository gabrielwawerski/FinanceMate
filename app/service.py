import ftplib
import util.settings as settings
import util.serializer as serializer

# app util/helper module
from account import Account
from transaction import AddTransaction, PayTransaction, TransactionType

ftp = ftplib.FTP(settings.ftp_host, settings.ftp_username, settings.ftp_password)


class Service:
    def __init__(self):
        self.settings = settings.app_settings

    def ftp_retrieve(self, path, filename, data_type):
        with open(f"data/{filename}", "wb") as server_file:
            data = ftp.retrbinary(f"RETR {path}/{filename}", server_file.write)

    def addtrans(self, _account, amount):
        self.add_acc_bal(_account, amount)
        return AddTransaction(self.next_trans_id(), _account, amount)

    def paytrans(self, _account, amount):
        self.sub_acc_bal(_account, amount)
        return PayTransaction(self.next_trans_id(), _account, amount)

    def add_account(self):
        return self

    def account_info(self):
        return self

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
        self.settings.set_setting("trans_uid", _trans_uid + 1)
        return int(_trans_uid)

    def set_default_settings(self):
        self.settings.load(self.from_server())

    def from_server(self):
        import requests
        import jsonpickle

        data = requests.get(f"{settings.full_data_url}{settings.default_settings}").text
        return dict(jsonpickle.decode(data))

    def get_acc_uid(self):
        return self.settings.get_setting("acc_uid")

    def get_trans_uid(self):
        return self.settings.get_setting("trans_uid")

    def get_currency(self):
        return self.settings.get_setting("currency")

    def get_max_balance(self):
        return self.settings.get_setting("max_balance")

    def get_timeout(self, ):
        return self.settings.get_setting("timeout")


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
