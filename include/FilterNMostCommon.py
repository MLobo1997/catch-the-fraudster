from sklearn.base import BaseEstimator, TransformerMixin


class FilterNMostCommon(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_name, N=10, minRelFreq=None, copy=True):
        self.N = N
        self.attribute_name = attribute_name
        self.copy = copy
        self.minRelFreq = minRelFreq

    def fit(self, X, y=None):
        # value_counts returns the values sorted by quantity so we just need to take the first N.
        value_counts = X[self.attribute_name].value_counts()[:self.N]

        if self.minRelFreq is not None:
            vc_ratio = value_counts / X.shape[0]
            self.values_that_stay = []
            for idx in range(vc_ratio.shape[0]):
                if vc_ratio[idx] > 0.05:
                    self.values_that_stay.append(vc_ratio.index[idx])
                else:
                    break
        else:
            self.values_that_stay = value_counts.index

        return self

    def transform(self, X):
        if self.copy:
            X = X.copy()
        X[self.attribute_name] = [
            val if val in self.values_that_stay else 'Other' for val in X[self.attribute_name]
        ]

        return X
