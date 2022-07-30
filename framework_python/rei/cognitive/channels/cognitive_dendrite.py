import abc

from rei.cognitive.channels.channel_base_definitions import CognitiveChannelDendrite, CognitiveIcon
from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkRelation, EnumRelationDirection
from rei.cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge

import queue

import numpy as np


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
        self.cnt_elem = 0

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

    def _setup_tensor_eslice(self, indices: queue.Queue, e: HypergraphEdge):
        # TODO: this is a naive implementation it can be done faster!
        ind_e = self.homomorphism_edge[e.uid]
        visited_pairs = set()
        # Get parent relationship
        if e.parent.uid in self.homomorphism_node:
            indices.put((-1, self.homomorphism_node[e.parent.uid], ind_e, 1))
            #self.cnt_elem += 1
        # Iterate through relations
        for relation in e.subset_elements:
            ind_n = self.homomorphism_node[relation.endpoint.uid]
            for other in e.subset_elements:
                if other is not relation:
                    # Sanitize values
                    value = HypergraphTensorTransformation._setup_value(relation.value)
                    # Get pair
                    _pair = (ind_n, self.homomorphism_node[other.endpoint.uid])
                    if _pair not in visited_pairs:
                        visited_pairs.add(_pair)
                        visited_pairs.add((_pair[1], _pair[0]))
                        match relation.direction:
                            case EnumRelationDirection.UNDIRECTED:
                                indices.put((_pair[0], _pair[1], ind_e, value))
                                indices.put((_pair[1], _pair[0], ind_e, value))
                                # Put incidence
                                indices.put((_pair[0], -1, ind_e, 1))
                                indices.put((_pair[1], -1, ind_e, 1))
                                self.cnt_elem += 4
                            case EnumRelationDirection.INWARDS:
                                indices.put((_pair[0], _pair[1], ind_e, -value))
                                indices.put((_pair[1], _pair[0], ind_e,  value))
                                indices.put((_pair[0], -1, ind_e, 1))
                                indices.put((_pair[1], -1, ind_e, -1))
                                self.cnt_elem += 4
                            case EnumRelationDirection.OUTWARDS:
                                indices.put((_pair[1], _pair[0], ind_e, -value))
                                indices.put((_pair[0], _pair[1], ind_e,  value))
                                indices.put((_pair[0], -1, ind_e, -1))
                                indices.put((_pair[1], -1, ind_e, 1))
                                self.cnt_elem += 4

    def _setup_tensor_hierarchy(self, indices: queue.Queue, n: HypergraphNode):
        for v in n.subset_elements:
            if isinstance(v, HypergraphNode):
                p = (self.homomorphism_node[n.uid], self.homomorphism_node[v.uid])
                indices.put((p[1], p[0], -1,  1))
                indices.put((p[0], p[1], -1, -1))
                self.cnt_elem += 1

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
        self.cnt_elem = 0

    @abc.abstractmethod
    def _setup_icon(self, indices: queue.Queue):
        raise NotImplementedError

    @abc.abstractmethod
    def _setup_intermediate_tensor(self):
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
        indices = queue.LifoQueue()
        while not self.edge_fringe.empty():
            e: HypergraphEdge = self.edge_fringe.get()
            self._setup_tensor_eslice(indices, e)
            self.cnt_elem += 1
        while not self.node_fringe.empty():
            n: HypergraphNode = self.node_fringe.get()
            self._setup_tensor_hierarchy(indices, n)
            self.cnt_elem += 1
        self._setup_intermediate_tensor()
        self._setup_icon(indices)
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

    def _setup_icon(self, indices: queue.Queue):
        while not indices.empty():
            x, y, z, v = indices.get()
            self.intermediate_tensor[z, y, x] = v

    def decode(self, arg):
        if self.intermediate_tensor is None:
            return None

    def _setup_intermediate_tensor(self):
        # Append additional dimension for hierarchy
        # Additional dimension for edge incidence
        # Additional dimension for edge hierarchy
        # DIMS: [EDGES, NODES+INCIDENCE, NODES+EDGE_HIERARCHY]
        self.intermediate_tensor = np.zeros(shape=(self.cnt_edges + 1, self.cnt_node + 1, self.cnt_node + 1))

    def _get_msg_tensor(self):
        return [self.intermediate_tensor]


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
        return [self.cnt_node, self.cnt_edges, self.cnt_elem,
                list(self.homomorphism_node.keys()),
                list(self.homomorphism_edge.keys()),
                self.intermediate_tensor.tolist(),
                self.value_tensor.tolist()]

    def _setup_intermediate_tensor(self):
        self.intermediate_tensor = np.zeros(shape=(self.cnt_elem, 3), dtype=np.int)
        self.value_tensor = np.zeros(shape=(self.cnt_elem, 1))

    def set_icon(self, e: CognitiveIcon):
        self._endpoint = e
