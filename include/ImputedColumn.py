from sklearn.base import BaseEstimator, TransformerMixin

class ImputedColumn(BaseEstimator, TransformerMixin):
    
    def __init__(self, missing_value, target_column, new_column, copy=True):
       self.missing_value = missing_value 
       self.target_column = target_column
       self.new_column = new_column
       self.copy = copy
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if self.copy:
            X = X.copy()
        
        X[self.new_column] = [1 if value == self.missing_value else 0 for value in X[self.target_column]]

        return X