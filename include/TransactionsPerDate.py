from copy import deepcopy

def sumTuples(tupleA, tupleB):
    return tuple([a + b for a, b in zip(tupleA, tupleB)])

class TransactionsPerDate():

    def __init__(self):
        self.transactions = {}

    def insertTransaction(self, user, datetime, amount):
        if user not in self.transactions:
            self.transactions[user] = {}
        if datetime.date() not in self.transactions[user]:
            self.transactions[user][datetime.date()] = (1, amount)
        else:
            user_day_content = self.transactions[user][datetime.date()]
            new_values = (1, amount)
            self.transactions[user][datetime.date()] = sumTuples(user_day_content, new_values)
    
    def getTransactionAveragesExceptDay(self, user, datetime):
        curr_date = datetime.date()
        user_transaction_measures = {}
        for date in self.transactions[user]:
            if date < curr_date:
                user_transaction_measures[date]  = self.transactions[user][date]

        N = len(user_transaction_measures)
        if N != 0:
            tuple_sum = (0,0)
            for _, tran in user_transaction_measures.items():
                tuple_sum = sumTuples(tuple_sum, tran)
            return tuple([x / N for x in tuple_sum])
        else:
            return (1,188.0)

    def getTransactionsDay(self, user, datetime):
        return self.transactions[user][datetime.date()]