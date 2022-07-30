import abc
from enum import IntEnum


class InterfaceNetworkSystem(metaclass=abc.ABCMeta):
    """
    A network (graph) containing nodes and relations as (hyper)edges.

    Can be transformed to a E-adjacency based representation
    """

    def addNode(self)-> None:
        """

        Add node as a structural element

        """
        raise NotImplementedError

class EnumHybridSystemState(IntEnum):
    PROPAGATED= 0
    SUSPENDED = 1
    ERROR = -1


class EnumMemoryOperation(IntEnum):
    TRANSMIT = 0
    FORGET = 1
    DECAY = 2


class InterfaceHybridSystem(metaclass=abc.ABCMeta):
    """
    Hybrid system attributed by discrete and continuous-time behavior
    Can be stimulated by discrete signals/events or variable delay

    The system is synchronized by a clock to step the system according
    to specific rules.
    """
    def set_clock(self) -> None:
        """
        Set the control clock
        :return:
        """

    def propagate(self) -> EnumHybridSystemState:
        """
        Propagate the system (add as callback to a clock)

        :return: a hybrid state enumeration indicating the result of propagation
        """
        raise NotImplementedError


class IClassifiable(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):

        return (hasattr(subclass, 'get_cluster_name') and
                callable(cls.get_cluster_name) and
                hasattr(subclass, 'get_cluster_id') and
                callable(cls.get_cluster_id) and
                hasattr(subclass, 'classify') and
                callable(cls.classify) or
                NotImplemented
                )

    @abc.abstractmethod
    def get_cluster_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_cluster_id(self) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def classify(self, concept):
        raise NotImplementedError
