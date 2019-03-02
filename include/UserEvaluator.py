from sklearn.base import BaseEstimator, TransformerMixin

class UserEvaluator(BaseEstimator, TransformerMixin):

    def __init__(self, column_names, copy=True):
        self.copy=copy
        self.column_names = column_names
        self.users={}
        self.k = ['N', 'amountSum']

    def fit(self, X, y=None):
        k = self.k
        for row in X.itertuples():
            if row[self.column_names.index('card_id')] not in self.users:
                userData = (1, row[self.column_names.index('amount')])
                self.users[row[self.column_names.index('card_id')]] = userData
            else:
                userData = self.users[row[self.column_names.index('card_id')]]
                N = userData[k.index('N')] + 1
                amountSum = userData[k.index('amountSum')] + row[self.column_names.index('amount')]
                self.users[row[self.column_names.index('card_id')]] = (N, amountSum)
        print(self.users)
        return self

    def transform(self, X):
        return X