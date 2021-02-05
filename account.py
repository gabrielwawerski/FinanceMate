import util.settings as settings


class Account:
    def __init__(self, uid, name='Client', account_balance=0):
        self.id = uid
        self.name = name
        self.balance = float(account_balance)

    def add_balance(self, amount):
        amt = self._check(amount)
        self.balance += amt

    def sub_balance(self, amount):
        amt = self._check(amount)
        self.balance -= amt

    # TODO: move checking to service.py - only validated data here! (move logic up)
    def _check(self, value):
        val, max_bal = value, settings.get_max_balance()

        if not isinstance(val, float):
            print(f"Amount({val}) is not a float! Converting...")
            val = float(val)

        if self.balance - val < 0:
            raise ValueError(f"Balance can't be lower than 0! What would balance be: {self.balance - val}")
        elif self.balance + val > max_bal:
            raise ValueError(f"Balance can't be higher than {max_bal}! What would balance be: {self.balance + val}")

        return val
