import abc

from cognitive.format.basicelements.concepts.network.base_definitions import NetworkRelation, NetworkNode, \
    NetworkElement, EnumRelationDirection
from cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, \
    HypergraphEdge, HyperEdgeConnection

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
        self.node_fringe = queue.LifoQueue()
        self.edge_fringe = queue.LifoQueue()
        self.intermediate_tensor = None

    def _collect_tensor_elements(self, cursor: HypergraphNode):
        """

        :param cursor:
        :return:
        """
        for c in cursor.subset_elements:
            match c:
                case HypergraphNode():
                    self.homomorphism_node[c.uid] = self.cnt_node
                    self.homomorphism_node_inv[self.cnt_node] = c.uid
                    self.node_fringe.put(c)
                    self.cnt_node += 1
                    self._collect_tensor_elements(c)
                case HypergraphEdge():
                    self.homomorphism_edge[c.uid] = self.cnt_edges
                    self.homomorphism_edge_inv[self.cnt_edges] = c.uid
                    self.edge_fringe.put(c)
                    self.cnt_edges += 1


class HypergraphTensorTransformation(TensorChannelDendrite):
    """

    """

    def encode(self, arg: list[HypergraphNode]):
        self.node_fringe = queue.LifoQueue()
        self.edge_fringe = queue.LifoQueue()
        self.cnt_node = 0
        self.cnt_edges = 0
        self.homomorphism_edge = {}
        self.homomorphism_edge_inv = {}
        self.homomorphism_node = {}
        self.homomorphism_node_inv = {}
        #
        for c in arg:
            self._collect_tensor_elements(c)
        self.intermediate_tensor = np.zeros((self.cnt_edges, self.cnt_node, self.cnt_node))
        # Traverse
        indices = queue.LifoQueue()
        while not self.edge_fringe.empty():
            e: HypergraphEdge = self.edge_fringe.get()
            ind_e = self.homomorphism_edge[e.uid]
            # TODO: finish this mess
            """
            for rel1 in e.subset_elements:
                ind_n = self.homomorphism_node[rel1.endpoint.uid]
                for rel0 in e.subset_elements:
                    if rel0 is not rel1:
                        if rel0.direction is EnumRelationDirection.OUTWARDS or rel0.direction is EnumRelationDirection.UNDIRECTED:
                            indices.put((ind_n, self.homomorphism_node[rel0.endpoint.uid], ind_e, rel0.value))
                        else:
                            indices.put((ind_n, self.homomorphism_node[rel0.endpoint.uid], ind_e, -rel0.value))
            """
            visited_pairs = set()
            # TODO: this is a naive implementation it can be done faster!
            for relation in e.subset_elements:
                ind_n = self.homomorphism_node[relation.endpoint.uid]
                for other in e.subset_elements:
                    _pair = (ind_n, self.homomorphism_node[other.endpoint.uid])
                    if _pair not in visited_pairs:
                        visited_pairs.add(_pair)
                        if other is not relation:
                            match relation.direction:
                                case EnumRelationDirection.UNDIRECTED:
                                    indices.put((_pair[0], _pair[1], ind_e, relation.value))
                                    indices.put((_pair[1], _pair[0], ind_e, relation.value))
                                case EnumRelationDirection.INWARDS:
                                    indices.put((_pair[0], _pair[1], ind_e, -relation.value))
                                    indices.put((_pair[1], _pair[0], ind_e,  relation.value))
                                case EnumRelationDirection.OUTWARDS:
                                    indices.put((_pair[1], _pair[0], ind_e, -relation.value))
                                    indices.put((_pair[0], _pair[1], ind_e,  relation.value))



            #for rel0 in e.subset_elements:
                #    if rel0 is not relation:
                #        if rel0.direction is EnumRelationDirection.OUTWARDS or rel0.direction is EnumRelationDirection.UNDIRECTED:
                #            indices.put((ind_n, self.homomorphism_node[rel0.endpoint.uid], ind_e, rel0.value))
                #        else:
                #            indices.put((ind_n, self.homomorphism_node[rel0.endpoint.uid], ind_e, -rel0.value))

        while not indices.empty():
            x, y, z, v = indices.get()
            self.intermediate_tensor[z, y, x] = v
        return self.intermediate_tensor

    def decode(self, arg):
        if self.intermediate_tensor is None:
            return None
