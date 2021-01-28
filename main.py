from transaction import Transaction
from account import Account
from app.app import *

if __name__ == '__main__':
    app = App()
    app.run()
    # app.newAccount("Mateusz Mateuszecki", "0")
    # app.newAccount("Modem Internacki", "1342")
    # app.newAccount("Kloszard Olbrychski", "12032")
    # app.newAccount("Kazmirz Brodacki", "2436")
    app.save_data()
    # app.loadData()
    # app.listAccounts()
    # app.quit()

