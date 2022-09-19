import abc
import asyncio

import numpy as np

from rei.foundations.graph_monad import GraphMonad
from rei.hypergraph.base_elements import HypergraphNode


class FuzzyNorm(HypergraphNode):

    @abc.abstractmethod
    def eval(self, x):
        raise NotImplementedError


class SNorm(FuzzyNorm):
    pass


class MaxNorm(SNorm):

    def eval(self, x):
        return np.max(x, axis=1)


class TNorm(FuzzyNorm):
    pass


class MinNorm(TNorm):

    def eval(self, x):
        return np.min(x, axis=1)


