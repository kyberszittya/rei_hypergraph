import queue

import cognitive.format.hypergraph.foundations.graph_operations as qu
from cognitive.format.basicelements.concepts.registry.registration_methods import \
    InterfaceIdentifierGenerator
from cognitive.format.basicelements.concepts.network.base_definitions import NetworkElement, EnumRelationDirection
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge, \
    HypergraphReferenceConnection, HyperEdgeConnection


class HypergraphCompartmentQuery(qu.MetaHypergraphQuery):
    """
    Query the components (subsets) of a given hypergraph(node)
    """

    def __init__(self, cursor: NetworkElement, id_name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(cursor, id_name, timestamp, identitygen)
        self._parameters["closed_elements"] = set()

    @staticmethod
    def _lookup_hierarchy(cursor: NetworkElement, lookup_name: str, closed_set: set[NetworkElement]):
        if cursor.progenitor_registry.qualified_name == lookup_name:
            yield cursor
        else:
            for v in cursor._subsets.values():
                if v not in closed_set:
                    yield from HypergraphCompartmentQuery._lookup_hierarchy(v, lookup_name, closed_set)

    def execute(self):
        for c in self._cursor:
            yield from HypergraphCompartmentQuery._lookup_hierarchy(c,
                                                                    self._parameters["lookup_name"],
                                                                    self._parameters["closed_elements"])

    def set_lookup_name(self, lookup_name: str):
        self._parameters["lookup_name"] = lookup_name

    def set_closed_elements(self, arg: set[NetworkElement]):
        self._parameters["closed_elements"] = arg


def retrieve_part_hypergraph_node(context: HypergraphNode, qualified_name: str):
    query = HypergraphCompartmentQuery(context, "lookup_query", 0)
    query.set_lookup_name(qualified_name)
    return query.execute()


class HypergraphBidirectionalCompartmentQuery(HypergraphCompartmentQuery):
    """

    """

    def __init__(self, cursor: NetworkElement, id_name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(cursor, id_name, timestamp, identitygen)

    def execute(self):
        closed_set: set = self._parameters["closed_elements"]
        for cursor in self._cursor:
            _current_cursor = cursor
            while _current_cursor is not None:
                yield from HypergraphCompartmentQuery. \
                    _lookup_hierarchy(_current_cursor, self._parameters["lookup_name"],
                                      closed_set)
                closed_set.add(_current_cursor)
                _current_cursor = _current_cursor.parent


class HypergraphDepthBidirectionalCompartmentQuery(HypergraphCompartmentQuery):
    """

    """

    def __init__(self, cursor: NetworkElement, id_name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(cursor, id_name, timestamp, identitygen)

    @staticmethod
    def _depth_lookup_hierarchy(cursor: NetworkElement, lookup_name: str,
                                closed_set: set[NetworkElement],
                                current_depth: int, depth_limit: int):
        if cursor.progenitor_registry.qualified_name == lookup_name and current_depth==depth_limit:
            yield cursor
        else:
            for v in cursor._subsets.values():
                if v not in closed_set:
                    yield from HypergraphDepthBidirectionalCompartmentQuery \
                        ._depth_lookup_hierarchy(v, lookup_name, closed_set, current_depth+1, depth_limit)

    def execute(self):
        current_depth = 0
        closed_set: set = self._parameters["closed_elements"]
        for cursor in self._cursor:
            _current_cursor = cursor
            while _current_cursor is not None:
                yield from HypergraphDepthBidirectionalCompartmentQuery. \
                    _depth_lookup_hierarchy(_current_cursor, self._parameters["lookup_name"],
                                            closed_set, 0, current_depth)
                closed_set.add(_current_cursor)
                _current_cursor = _current_cursor.parent
                current_depth += 1


class HypergraphEdgeDirectConnectNodes(qu.MetaHypergraphQuery):
    """

    """

    def __init__(self, cursor: NetworkElement, id_name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(cursor, id_name, timestamp, identitygen)
        self._parameters["endpoints"]: list[tuple[str, EnumRelationDirection]] = []

    def add_endpoint_node(self, qualified_name: str,
                          direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        self._parameters["endpoints"].append((qualified_name, direction))

    def execute(self):
        query = HypergraphBidirectionalCompartmentQuery(self._cursor,
                                                        self.id_name+f"{self._timestamp}_connect",
                                                        self.timestamp, self._identitygen)
        edge = HypergraphEdge(self.id_name, self.timestamp, self._cursor[0], self._identitygen)
        for n in self._parameters["endpoints"]:
            query.set_lookup_name(n[0])
            query.set_cursor_node(self._cursor[0], self.timestamp)
            r = list(query.execute())[0]
            edge.connect(r, 1.0, self.timestamp, n[1])
        return edge


def create_hyperedge(name: str, timestamp: int, parent: HypergraphNode,
                     connections: list[tuple[str, EnumRelationDirection]]) -> HypergraphEdge:
    """
    Create a hyperedge with parameters

    :param name: name of the edge
    :param timestamp: timestamp of edge
    :param parent: the hyperedge parent node (set element)
    :param connections: each node connection
    :return: the hyperedge
    """
    query = HypergraphEdgeDirectConnectNodes(parent, name, timestamp)
    for conn in connections:
        query.add_endpoint_node(conn[0], conn[1])
    return query.execute()


def create_hypergraphelement_reference(ref_name, root: HypergraphNode, referenced: HypergraphNode):
    ref_id = "ref_"+ref_name
    # Try to retrieve referenced item
    _lookup_name = '/'.join([root.progenitor_registry.qualified_name, ref_name])
    ref_res = list(retrieve_part_hypergraph_node(root, _lookup_name))
    # Try to retrieve element
    _edge_element_name = '/'.join([root.progenitor_registry.qualified_name, ref_id])
    res = list(retrieve_part_hypergraph_node(root, _edge_element_name))
    if len(res) == 0:
        ref_edge = HypergraphEdge(ref_id, 0, root)
        root.add_subset(ref_edge, 0)
        # To reference
        ref_conn = HypergraphReferenceConnection(f"{ref_name}_ref", 0, ref_edge.domain, ref_edge)
        ref_edge.add_connection(ref_conn, 0, ref_res[0], EnumRelationDirection.INWARDS)
        # Connect to current link
        ref_conn = HypergraphReferenceConnection(f"{ref_name}_{ref_id}", 0,
                                                 ref_edge.domain, ref_edge)
        ref_edge.add_connection(ref_conn, 0, referenced, EnumRelationDirection.OUTWARDS)
    else:
        ref_conn = HypergraphReferenceConnection(f"{ref_name}_{ref_id}", 0,
                                                 res[0].domain, res[0])
        res[0].add_connection(ref_conn, 0, referenced, EnumRelationDirection.OUTWARDS)


def hypergraphedge_2factorization_tree(edge: HypergraphEdge):
    incoming_edges = []
    outgoing_edges = []
    for e in filter(lambda x: isinstance(x, HyperEdgeConnection), edge._subsets.values()):
        match e.direction:
            case EnumRelationDirection.INWARDS:
                incoming_edges.append(e)
            case EnumRelationDirection.OUTWARDS:
                outgoing_edges.append(e)
            case EnumRelationDirection.UNDIRECTED:
                outgoing_edges.append(e)
                incoming_edges.append(e)
    # Descartes combination
    res = queue.Queue()
    for c0 in incoming_edges:
        for c1 in outgoing_edges:
            res.put((c0, c1))
    return res
