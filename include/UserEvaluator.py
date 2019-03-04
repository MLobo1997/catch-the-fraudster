from sklearn.base import BaseEstimator, TransformerMixin
from include.TransactionsPerDate import TransactionsPerDate
from pandas import Timestamp


def divTuples(tupleA, tupleB):
    return tuple([a / b for a, b in zip(tupleA, tupleB)])


class UserEvaluator(BaseEstimator, TransformerMixin):

    def __init__(self, use_card = False, N_attribute_name='daily_transactions_ratio', amount_attribute_name='amount_transactions_ratio', copy=True):
        self.copy = copy
        self.transactions = TransactionsPerDate()
        self.first = True
        self.N_attribute_name = N_attribute_name
        self.amount_attribute_name = amount_attribute_name
        if use_card:
            self.user_attr='user_id'
        else:
            self.user_attr='card_id'

    def createTransactions(self, X):
        names = list(X)
        for row in X.itertuples(index=False):
            user = row[names.index(self.user_attr)]
            datetime = row[names.index('datetime')]
            amount = row[names.index('amount')]
            self.transactions.insertTransaction(
                user,
                datetime,
                amount,
            )

    def fit(self, X, y=None):
        self.createTransactions(X)
        return self

    def transform(self, X):
        if self.copy:
            X = X.copy()

        if self.first:
            self.first = False
        else:
            self.createTransactions(X)
        
        new_attr = [
            divTuples(self.transactions.getTransactionsDay(user, datetime),
                      self.transactions.getTransactionAveragesExceptDay(user, datetime))
            for user, datetime in zip(X[self.user_attr], X['datetime'])
        ]

        a, b = zip(*new_attr)
        X[self.N_attribute_name], X[self.amount_attribute_name] = list(a), list(b)

        return X
