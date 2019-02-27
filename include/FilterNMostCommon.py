from sklearn.base import BaseEstimator, TransformerMixin

class FilterNMostCommon(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_name, N = 10, copy = True):
        self.N = N
        self.attribute_name = attribute_name
        self.copy = copy

    def fit(self, X, y = None):
        self.values_that_stay = X[self.attribute_name].value_counts().index[:self.N] #value_counts returns the values sorted by quantity
                                                                                            #so we just need to take the first N.
        return self

    def transform(self, X):
        if self.copy:
            X = X.copy()
        X[self.attribute_name] = [ val if val in self.values_that_stay else 'Other' for val in X[self.attribute_name] ]
        return X