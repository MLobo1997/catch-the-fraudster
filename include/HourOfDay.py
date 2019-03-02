from sklearn.base import BaseEstimator, TransformerMixin
from datetime import datetime

class HourOfDay(BaseEstimator, TransformerMixin):

    def __init__(self, timestamp_attribute='timestamp', new_attribute='hour', copy = True):
        self.timestamp_attribute = timestamp_attribute
        self.new_attribute = new_attribute
        self.copy = copy

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.copy:
            X = X.copy()
        
        X[self.new_attribute] = [datetime.utcfromtimestamp(int(ts) / 1000).time().hour for ts in X[self.timestamp_attribute]]

        return X