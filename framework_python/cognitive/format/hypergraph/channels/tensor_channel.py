import abc

from cognitive.format.basicelements.concepts.network.base_definitions import NetworkRelation, NetworkNode, \
    NetworkElement, EnumRelationDirection
from cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge, HyperEdgeConnection

import numpy as np


import queue

class CognitiveArbiter(HypergraphNode):
    """

    """


class CognitiveIcon(HypergraphNode):
    """
    A cognitive icon of some sort (e.g. image (2D matrix), stimuli, tensor)
    """
    @abc.abstractmethod
    def view(self):
        raise NotImplementedError


class TensorCognitiveIcon(CognitiveIcon):
    """

    """

    def __init__(self, name: str, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self._icon = []

    def view(self):
        return self._icon


class CognitiveChannelDendrite(HyperEdgeConnection):
    """

    """
    @abc.abstractmethod
    def encode(self, arg):
        raise NotImplementedError

    @abc.abstractmethod
    def decode(self, arg):
        raise NotImplementedError


class CognitiveChannel(HypergraphEdge):
    """

    """



class TensorChannelDendrite(CognitiveChannelDendrite):
    """

    """

    def __init__(self, name: str, timestamp: int, domain: MetaRegistry, parent: NetworkRelation,
                 endpoint: HypergraphNode, value=None, identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, domain, parent, endpoint, value, identitygen, direction)
        # Mappings (as per identifier)
        self.homomorphism_node = {}
        self.homomorphism_node_inv = {}
        self.cnt_node = 0
        self.homomorphism_edge = {}
        self.homomorphism_edge_inv = {}
        self.cnt_edges = 0
        # Result tensor
        self.nodes = queue.LifoQueue()
        self.edges = queue.LifoQueue()
        self.tensor = None

    def _collect_tensor_elements(self, cursor: HypergraphNode):
        for c in cursor._subsets.values():
            if isinstance(c, HypergraphNode):
                self._collect_tensor_elements(c)
                self.homomorphism_node[c.uid] = self.cnt_node
                self.homomorphism_node_inv[self.cnt_node] = c.uid
                self.nodes.put(c)
                self.cnt_node += 1
            elif isinstance(c, HypergraphEdge):
                self.homomorphism_edge[c.uid] = self.cnt_edges
                self.homomorphism_edge_inv[self.cnt_edges] = c.uid
                self.edges.put(c)
                self.cnt_edges += 1


class HypergraphTensorTransformation(TensorChannelDendrite):
    """

    """

    def encode(self, arg: list[HypergraphNode]):
        self.nodes = queue.LifoQueue()
        self.edges = queue.LifoQueue()
        self.cnt_node = 0
        self.cnt_edges = 0
        self.homomorphism_edge = {}
        self.homomorphism_edge_inv = {}
        self.homomorphism_node = {}
        self.homomorphism_node_inv = {}
        #
        for c in arg:
            self._collect_tensor_elements(c)
        self.tensor = np.zeros((self.cnt_edges, self.cnt_node, self.cnt_node))
        # Traverse
        indices = queue.LifoQueue()
        while not self.edges.empty():
            e: HypergraphEdge = self.edges.get()
            ind_e = self.homomorphism_edge[e.uid]
            for rel1 in e._subsets.values():
                ind_n = self.homomorphism_node[rel1.endpoint.uid]
                for rel0 in e._subsets.values():
                    if rel0 is not rel1:
                        indices.put((ind_n, self.homomorphism_node[rel0.endpoint.uid], ind_e, rel0.value))
        while not indices.empty():
            x,y,z,v = indices.get()
            self.tensor[z,y,x] = v
        return self.tensor


    def decode(self, arg):
        if self.tensor is None:
            return None



