
from cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from cognitive.format.basicelements.concepts.registry.registration_methods import \
    InterfaceIdentifierGenerator, IdentifierGeneratorSha224
from cognitive.format.basicelements.concepts.network.base_definitions import NetworkNode, \
    NetworkRelation, EnumRelationDirection, NetworkElement

import lxml


class HypergraphNode(NetworkNode):
    """
    A netowrk node that can be extended as a hierarchy of multisets, and connected via
    hypergraph edges.

    A hypergraph consists hypergraph nodes as subset elements
    """


    def __init__(self, name: str, timestamp: int,
                 subsets: dict[bytes, NetworkElement] = None, parent: NetworkNode = None,
                 identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, identitygen, domain, parent)
        # Storing subsets as a tree
        if subsets is not None:
            self._subsets: dict[bytes, NetworkElement] = subsets

    def add_subset(self, s: NetworkElement, timestamp: int) -> None:
        """
        Add a node to the hierarchy

        :param s: item to be added as a network element
        :param timestamp: timestamp of subset addition
        :return:
        """
        self._subsets[s.uid] = s
        s.parent = self
        # Identification and registry
        idgen = IdentifierGeneratorSha224(prefix='/'.join([self.domain.name, self.id_name]))
        s.reidentify(idgen)
        s.register(self._taxonomy, timestamp)

    def print_hierarchy_tree(self, prefix=''):
        print(f"{prefix}-> {self.uid.hex()}: {self.progenitor_registry.name}")
        for s in self._subsets.values():
            if isinstance(s, HypergraphNode):
                s.print_hierarchy_tree(prefix+'\t')
            elif isinstance(s, HypergraphEdge):
                s.print_elements()

    def __iadd__(self, other: NetworkElement):
        self.add_subset(other, self.timestamp)
        return self


class HyperEdgeConnection(NetworkRelation):
    """
    Associated relation with the network node
    """

    def __init__(self, name: str, timestamp: int, domain: MetaRegistry = None,
                 parent: NetworkRelation = None,
                 endpoint: HypergraphNode = None, value = None,
                 identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, domain, identitygen, parent, direction)
        self._endpoint: HypergraphNode = endpoint
        self.value = value

    @property
    def endpoint(self):
        return self._endpoint

    def update(self, edge: NetworkRelation, domain, timestamp: int,
               endpoint: HypergraphNode, direction: EnumRelationDirection):
        if self.domain is not domain:
            self.register(domain, timestamp)
        self.parent = edge
        if direction is not None:
            self._direction = direction
        if endpoint is not None:
            self._endpoint = endpoint
            #edge._subsets[endpoint.uid] = self


class HypergraphEdge(NetworkRelation):
    """
    A relation that can have multiple endpoints
    """

    def __init__(self, name: str, timestamp: int,
                 parent: HypergraphNode, identitygen: InterfaceIdentifierGenerator=None):
        super().__init__(name, timestamp, parent._taxonomy, identitygen, parent)

    def connect(self, node: HypergraphNode,
                value, timestamp: int,
                direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED) -> None:
        """

        :param node: node to be added
        :param value: arbitrary value associated with the edge
        :param timestamp: connection timestamp
        :param direction: top-level direction of the edge
        :return: nothing
        """
        c1 = HyperEdgeConnection('/'.join([self.id_name,node.id_name]),
                                 timestamp, self.domain,
                                 self, node, value, self._identitygen, direction)
        self.add_connection(c1, timestamp)
        #c1.parent = self
        #self._subsets[node.uid] = c1

        """
        c1 = HyperEdgeConnection('/'.join([self.id_name,node.id_name]),
                                 timestamp, self.domain,
                                 self, node, value, self._identitygen, direction)
        self.add_connection(c1, timestamp)
        """


    def add_connection(self,
                       conn: HyperEdgeConnection,
                       timestamp: int,
                       node_endpoint: HypergraphNode = None,
                       direction: EnumRelationDirection = None) -> None:
        """

        :param node: node to be added
        :param timestamp: connection timestamp
        :param conn: connection to be added to the edge
        :param direction: top-level direction of the edge
        :return: nothing
        """
        conn.update(self, self.domain, timestamp, node_endpoint, direction)
        if node_endpoint is not None:
            self._subsets[node_endpoint.uid] = conn
        else:
            self._subsets[conn.endpoint.uid] = conn
        """
        if conn.domain is not self.domain:
            conn.register(self.domain, timestamp)
        conn.parent = self
        if direction is not None:
            conn._direction = direction
        if node_endpoint is not None:
            conn._endpoint = node_endpoint
            self._subsets[node_endpoint.uid] = conn
        """

    def print_elements(self):
        hierarchy = self.id_name+": "
        for s in self._subsets.values():
            match s.direction:
                case EnumRelationDirection.INWARDS:
                    hierarchy += '<-'
                case EnumRelationDirection.OUTWARDS:
                    hierarchy += '->'
                case EnumRelationDirection.UNDIRECTED:
                    hierarchy += '--'
            hierarchy += s.endpoint.progenitor_registry.name + ', '
        print(hierarchy)

def select_incoming_connections(e: HypergraphEdge):
    res = []
    for _e in e._subsets.values():
        if isinstance(_e, HyperEdgeConnection):
            if _e.direction == EnumRelationDirection.INWARDS:
                res.append(_e)
    return res


class HypergraphReferenceConnection(HyperEdgeConnection):

    def __init__(self, name: str, timestamp: int, domain: MetaRegistry = None, parent: NetworkRelation = None,
                 endpoint: HypergraphNode = None, value=None, identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, domain, parent, endpoint, value, identitygen, direction)

    def update(self, edge: NetworkRelation, domain, timestamp: int, endpoint: HypergraphNode,
               direction: EnumRelationDirection):
        super().update(edge, domain, timestamp, endpoint, direction)
        # TODO: Create a function that adds subset but does not change parent
        endpoint._subsets[self.uid] = self



