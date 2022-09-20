import abc

import numpy as np

from rei.hypergraph.base_elements import HypergraphNode


class FuzzyNorm(HypergraphNode):

    @abc.abstractmethod
    def eval(self, x):
        raise NotImplementedError


class SNorm(FuzzyNorm):
    pass


class MaxNorm(SNorm):

    def eval(self, x, axis=1):
        return np.max(x, axis=axis)


class TNorm(FuzzyNorm):
    pass


class MinNorm(TNorm):

    def eval(self, x, axis=1):
        return np.min(x, axis=axis)


