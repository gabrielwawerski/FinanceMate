from transaction import Transaction
from account import Account
from app import *

if __name__ == '__main__':
    app = SimpleApp(name="Gabe", balance="100")
    app.newAccount("Mateusz Mateuszecki", "0")
    # app.newAccount("Kloszard Olbrychski", "12000")
    app.listAccounts()
    app.saveData()
    app.loadData()
    app.listAccounts()

