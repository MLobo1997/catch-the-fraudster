from sklearn.base import BaseEstimator, TransformerMixin
from datetime import datetime

class DatetimeFromTimestamp(BaseEstimator, TransformerMixin):
    def __init__(self, new_attribute_name = 'datetime', timestamp_attribute_name = 'timestamp', copy = True):
        self.new_attribute_name = new_attribute_name
        self.timestamp_attribute_name = timestamp_attribute_name 
        self.copy = copy

    def fit(self, X, y = None):
        return self

    def transform(self, X):
        if self.copy:
            X = X.copy()

        X[self.new_attribute_name] = [datetime.utcfromtimestamp(int(ts) / 1000) for ts in X[self.timestamp_attribute_name]] 
        return X