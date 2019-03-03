class Transactions():

    def __init__(self):
        self.transactions = {}

    def insertTransaction(self, user, id_num, datetime, amount):
        if user not in self.transactions:
            self.transactions[user] = {}
        self.transactions[user][id_num] = (datetime, amount)
    
    def getUser(self, user):
        if user in self.transactions:
            return self.transactions[user]
        else:
            raise ValueError('User ', user, ' not listed.') 