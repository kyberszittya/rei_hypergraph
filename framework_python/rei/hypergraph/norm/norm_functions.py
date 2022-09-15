import abc

import numpy as np


class NormFunctor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def norm(self, arg):
        raise NotImplementedError


class SNorm(NormFunctor, abc.ABC):
    pass


class TNorm(NormFunctor, abc.ABC):
    pass


class SumNorm(SNorm):

    def norm(self, arg):
        return np.sum(np.array(arg))


class ProdNorm(TNorm):

    def norm(self, arg):
        return np.array(arg) @ np.array(arg).T
