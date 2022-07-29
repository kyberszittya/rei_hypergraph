import abc

from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, \
    HypergraphEdge, HyperEdgeConnection


class CognitiveArbiter(HypergraphNode):
    """

    """


class CognitiveChannelDendrite(HyperEdgeConnection):
    """

    """
    @abc.abstractmethod
    def encode(self, arg) -> []:
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, arg):
        raise NotImplementedError


class CognitiveChannel(HypergraphEdge):
    """

    """


class CognitiveIcon(HypergraphNode):
    """
    A cognitive icon of some sort (e.g. image (2D matrix), stimuli, tensor)
    """

    @abc.abstractmethod
    def view(self):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, msg):
        raise NotImplementedError
