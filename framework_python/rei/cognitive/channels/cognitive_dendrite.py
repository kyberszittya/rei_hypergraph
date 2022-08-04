import abc

from rei.cognitive.channels.channel_base_definitions import CognitiveChannelDendrite, CognitiveIcon
from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkRelation, EnumRelationDirection
from rei.cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge

import queue

import numpy as np

from rei.cognitive.messages.message_fragment import FragmentMessage
from rei.cognitive.messages.tensor_fragment import FragmentTensor


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
        # Elements
        self.cnt_values = 0
        self.cnt_incidence = 0
        # Fragments
        self.fragment: FragmentMessage | None = None

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

    def _setup_tensor_eslice(self, indices: queue.Queue, indices_incidence: queue.Queue, e: HypergraphEdge):
        ind_e = self.homomorphism_edge[e.uid]
        # Get parent relationship
        # Iterate through relations to produce incidence relationships
        for relation in e.subrelations:
            ind_n = self.homomorphism_node[relation.endpoint.uid]
            match relation.direction:
                case EnumRelationDirection.UNDIRECTED:
                    indices_incidence.put((ind_n, ind_e, 1))
                case EnumRelationDirection.OUTWARDS:
                    indices_incidence.put((ind_n, ind_e, 1))
                case EnumRelationDirection.INWARDS:
                    indices_incidence.put((ind_n, ind_e, -1))
        # Value tensor setup
        for n0 in e.subrelations:
            for n1 in e.subrelations:
                if n0 is not n1:
                    value = HypergraphTensorTransformation._setup_value(n0.value)
                    _pair = (self.homomorphism_node[n0.endpoint.uid], self.homomorphism_node[n1.endpoint.uid])
                    match n0.direction:
                        case EnumRelationDirection.UNDIRECTED:
                            indices.put((_pair[0], _pair[1], ind_e, value))
                            indices.put((_pair[1], _pair[0], ind_e, value))
                            self.cnt_values += 2
                        case EnumRelationDirection.OUTWARDS:
                            indices.put((_pair[0], _pair[1], ind_e, value))
                            self.cnt_values += 1

    def _setup_tensor_node_hierarchy(self, indices_node: queue.Queue, context: HypergraphNode):
        for v in context.subset_elements:
            if isinstance(v, HypergraphNode):
                p = (self.homomorphism_node[context.uid], self.homomorphism_node[v.uid])
                indices_node.put((p[0], p[1], 1))

    def _setup_tensor_edge_hierarchy(self, indices_edge: queue.Queue, context: HypergraphNode):
        for v in context.subset_elements:
            if isinstance(v, HypergraphEdge):
                p = (self.homomorphism_node[context.uid], self.homomorphism_edge[v.uid])
                indices_edge.put((p[0], p[1], 1))

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

    @abc.abstractmethod
    def _setup_icon(self, indices_values: queue.Queue, indices_hierarchy: queue.Queue,
                    indices_adjacency: queue.Queue, indices_edge_hierarchy: queue.Queue):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_msg_tensor(self):
        raise NotImplementedError

    def encode(self, arg: list[HypergraphNode]):
        self._reset_homomorphism()
        #
        for c in arg:
            self._collect_tensor_elements(c)

        # Traverse
        indices_values = queue.LifoQueue()
        indices_hierarchy = queue.LifoQueue()
        indices_incidence = queue.LifoQueue()
        indices_edge_hierarchy = queue.LifoQueue()
        while not self.edge_fringe.empty():
            e: HypergraphEdge = self.edge_fringe.get()
            self._setup_tensor_eslice(indices_values, indices_incidence, e)
        while not self.node_fringe.empty():
            n: HypergraphNode = self.node_fringe.get()
            self._setup_tensor_node_hierarchy(indices_hierarchy, n)
            self._setup_tensor_edge_hierarchy(indices_edge_hierarchy, n)
        self._setup_icon(indices_values, indices_hierarchy, indices_incidence, indices_edge_hierarchy)
        if self.endpoint is not None:
            if isinstance(self.endpoint, CognitiveIcon):
                self.endpoint.update(self._get_msg_tensor())


class HypergraphTensorTransformation(TensorChannelDendrite):
    """

    """

    # TODO: think about generalization
    @staticmethod
    def _setup_value(arg):
        if arg is None:
            return 1.0
        return arg

    def _setup_icon(self,  indices_values: queue.Queue, indices_hierarchy: queue.Queue,
                    indices_incidence: queue.Queue, indices_edge_hierarchy: queue.Queue):
        # Values tensor
        _indices_tensor = np.zeros(shape=(self.cnt_node, self.cnt_node, self.cnt_edges))
        while not indices_values.empty():
            x, y, z, v = indices_values.get()
            _indices_tensor[x, y, z] = v
        # Indices hierarchy
        _indices_hierarchy = np.zeros(shape=(self.cnt_node, self.cnt_node))
        while not indices_hierarchy.empty():
            x, y, v = indices_hierarchy.get()
            _indices_hierarchy[x, y] = v
        # Indices incidence
        _indices_incidence = np.zeros(shape=(self.cnt_node, self.cnt_edges))
        while not indices_incidence.empty():
            x, y, v = indices_incidence.get()
            _indices_incidence[x, y] = v
        # Indices edge hierarchy
        _indices_edge_hierarchy = np.zeros(shape=(self.cnt_node, self.cnt_edges))
        while not indices_edge_hierarchy.empty():
            x, y, v = indices_edge_hierarchy.get()
            _indices_edge_hierarchy[y, x] = v
        # Fragment tensor
        self.fragment_tensor = FragmentTensor(_indices_tensor, _indices_hierarchy,
                                              _indices_incidence, _indices_edge_hierarchy)

    def decode(self, arg):
        if self.intermediate_tensor is None:
            return None

    def _get_msg_tensor(self):
        return [self.fragment_tensor]


class HypergraphCoordinateObject(TensorChannelDendrite):
    """

    """

    @staticmethod
    def _setup_value(arg):
        if arg is None:
            return 1.0
        return arg

    def _setup_icon(self, indices: queue.Queue):
        cnt = 0
        while not indices.empty():
            e = indices.get()
            self.intermediate_tensor[cnt, 0] = e[0]
            self.intermediate_tensor[cnt, 1] = e[1]
            self.intermediate_tensor[cnt, 2] = e[2]
            self.value_tensor[cnt] = e[3]
            cnt += 1

    def decode(self, arg):
        if self.intermediate_tensor is None:
            return None

    def _get_msg_tensor(self):
        return self.fragment

    def set_icon(self, e: CognitiveIcon):
        self._endpoint = e
