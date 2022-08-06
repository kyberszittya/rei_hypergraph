import abc
import queue

from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkRelation, EnumRelationDirection
from rei.cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator

from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, \
    HypergraphEdge, HyperEdgeConnection
from rei.cognitive.messages.message_fragment import FragmentMessage


class CognitiveArbiter(HypergraphNode):
    """

    """


class CognitiveChannelDendrite(HyperEdgeConnection):
    """

    """

    def __init__(self, name: str, timestamp: int, domain: MetaRegistry = None, parent: NetworkRelation = None,
                 endpoint: HypergraphNode = None, value=None, identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, domain, parent, endpoint, value, identitygen, direction)
        # Mappings (as per identifier)
        self.homomorphism_node = {}
        self.homomorphism_node_inv = {}
        self.cnt_node = 0
        self.homomorphism_edge = {}
        self.homomorphism_edge_inv = {}
        self.cnt_edges = 0
        self.cnt_relations = 0
        # Result tensor
        self.node_fringe = queue.LifoQueue()
        self.edge_fringe = queue.LifoQueue()
        # Elements
        self.cnt_values = 0
        self.cnt_incidence = 0
        # Fragments
        self.fragment: FragmentMessage | None = None

    @abc.abstractmethod
    def encode(self, arg) -> []:
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, arg):
        raise NotImplementedError

    def _reset_homomorphism(self):
        self.node_fringe = queue.LifoQueue()
        self.edge_fringe = queue.LifoQueue()
        self.cnt_node = 0
        self.cnt_edges = 0
        self.homomorphism_edge = {}
        self.homomorphism_edge_inv = {}
        self.homomorphism_node = {}
        self.homomorphism_node_inv = {}
        # Elements
        self.cnt_values = 0
        self.cnt_incidence = 0


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
