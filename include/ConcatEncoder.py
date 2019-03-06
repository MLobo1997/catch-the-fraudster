from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from functools import reduce
import operator

def mean(l):
    return reduce(lambda x, y: x+y, l) / len(l)

def groupByMean(concats, y):
    dictionary = {}

    for val, boolean in zip(concats, y):
        if val not in dictionary:
            dictionary[val] = [boolean]
        else:
            dictionary[val].append(boolean)

    return {k: mean(list_of_bools) for k, list_of_bools in dictionary.items()}

def filterByRelFreq(concats, min_rel_freq):
    N = len(concats)
    value_relative_counts = pd.Series(concats).value_counts() / N

    for idx, rel_freq in enumerate(value_relative_counts):
        if rel_freq < min_rel_freq:
            n = idx
            break

    acceptable = list(value_relative_counts[:n].index)
    return [val if val in acceptable else 'Other' for val in concats]

def sortDictionary(dictionary):
    list_of_tuples = sorted(dictionary.items(), key=operator.itemgetter(1))
    return  [x[0] for x in list_of_tuples]

def concat(X, attributes):
    concats = X[attributes[0]]
    attributes = attributes[1:]

    for attr in attributes:
        concats = [a + '-' + b for a,b in zip(concats, X[attr])]

    return concats

class ConcatEncoder(BaseEstimator, TransformerMixin):
    #This is not optimal if you want to concatenate many columns
    def __init__(self, attributes, attr_name, min_rel_freq=None, order_by_class=True, drop_old = True, copy=True):
        if len(attributes) < 2:
            raise ValueError('There need to be more than 1 attribute.')
        self.attributes = attributes
        self.copy = copy
        self.attr_name = attr_name
        self.min_rel_freq = min_rel_freq
        self.order_by_class = order_by_class
        self.drop_old = drop_old
    
    def fit(self, X, y=None):
        #creates the concatenated attribute
        concats = concat(X, self.attributes)
        
        #removing those smaller than the minimum relative frequency
        if self.min_rel_freq is not None:
            concats = filterByRelFreq(concats, self.min_rel_freq)
        
        #ranking values by class probability
        if self.order_by_class:
            dictionary = groupByMean(concats, y)
            self.rank = sortDictionary(dictionary)

        #just get the unique values
        else:
            self.rank = list(set(concats))

        return self

    def transform(self, X):
        if self.copy:
            X = X.copy()
        
        concats = concat(X, self.attributes)

        other_index = self.rank.index('Other')
        l = []
        for value in concats:
            try:
                label = self.rank.index(value)
            except ValueError:
                label = other_index
            l.append(label)

        X[self.attr_name] = l

        if self.drop_old:
            X.drop(self.attributes, axis=1)

        return X
