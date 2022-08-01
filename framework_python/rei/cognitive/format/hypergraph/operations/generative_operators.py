from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection, NetworkElement
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from rei.cognitive.format.hypergraph.foundations.graph_operations import MetaHypergraphQuery
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphEdge, HypergraphNode, \
    HypergraphReferenceConnection
from rei.cognitive.format.hypergraph.foundations.hypergraph_operators import HypergraphBidirectionalCompartmentQuery, \
    retrieve_part_hypergraph_node


class HypergraphEdgeDirectConnectNodes(MetaHypergraphQuery):
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
    """

    :param ref_name:
    :param root:
    :param referenced:
    :return:
    """
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


def create_dir_edge(sys: HypergraphNode, qualified_name: str, root_node: list[str], nodes: list[str]):
    e = create_hyperedge("e"+''.join(nodes), 0, sys, [(qualified_name+x, EnumRelationDirection.OUTWARDS) for x in nodes])
    for r in root_node:
        x = list(retrieve_part_hypergraph_node(sys, qualified_name+r))
        e.connect(x[0], 1.0, 0, EnumRelationDirection.INWARDS)
    sys.add_subset(e, 0)


def create_dir_simple_edge(sys: HypergraphNode, qualified_name: str, nodes: list[str]):
    e = create_hyperedge("e"+''.join(nodes), 0, sys, [(qualified_name+x, EnumRelationDirection.OUTWARDS) for x in nodes])
    sys.add_subset(e, 0)
