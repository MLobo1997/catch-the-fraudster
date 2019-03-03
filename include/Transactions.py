class Transactions():

    def __init__(self):
        self.transactions = {}

    def insertTransaction(self, user, datetime, amount):
        if user not in self.transactions:
            self.transactions[user] = [(datetime, amount)]
        else:
            self.transactions[user].append((datetime, amount))
    
    def getUser(self, user):
        if user in self.transactions:
            return self.transactions[user]
        else:
            raise ValueError('User ', user, ' not listed.') 