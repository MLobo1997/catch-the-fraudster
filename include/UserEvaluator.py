from sklearn.base import BaseEstimator, TransformerMixin
from include.Transactions import Transactions

class UserEvaluator(BaseEstimator, TransformerMixin):

    def __init__(self, col_names, copy=True):
        self.copy=copy
        self.col_names=col_names
        self.transactions=Transactions()

    def fit(self, X, y=None):
        for row in X.itertuples(index = False):
            user = row[self.col_names.index('user_id')]
            id_num = row[self.col_names.index('id')]
            datetime = row[self.col_names.index('datetime')]
            amount = row[self.col_names.index('amount')]
            self.transactions.insertTransaction(
                user,
                id_num,
                datetime,
                amount,
            )
        return self

    def transform(self, X):
        return X