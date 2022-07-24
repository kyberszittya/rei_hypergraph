from cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from cognitive.format.hypergraph.foundations.hypergraph_operators import \
    HypergraphCompartmentQuery, HypergraphDepthBidirectionalCompartmentQuery, \
    HypergraphBidirectionalCompartmentQuery, HypergraphEdgeDirectConnectNodes, \
    create_hyperedge
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge, \
    EnumRelationDirection
from cognitive.format.hypergraph.test.common_test_factories import SimpleTestFactory


def test_connect_hyperedge():
    """
    Test add simple
    :return:
    """
    _, test_system = SimpleTestFactory.create_4_nodes()
    # Add edge
    # Select first node
    query_name = "network_node/sys/node2"
    query = HypergraphCompartmentQuery(test_system, "query1", 0)
    query.set_lookup_name(query_name)
    node1 = list(query.execute())[0]
    # Select next node
    query_name = "network_node/sys/node1"
    query = HypergraphCompartmentQuery(test_system, "query2", 0)
    query.set_lookup_name(query_name)
    node2 = list(query.execute())[0]
    # Hypergraph edges
    edge = HypergraphEdge("test_edge", 0, test_system)
    # Connect
    edge.connect(node1, 1.0, 0)
    edge.connect(node2, 1.0, 0)
    for v in edge._subsets.values():
        assert v.parent is edge
    assert edge._subsets[node1.uid].endpoint is node1
    assert edge._subsets[node2.uid].endpoint is node2


def test_connect_hyperedge_directed():
    """
    Test add simple
    :return:
    """
    _, test_system = SimpleTestFactory.create_4_nodes()
    # Add edge
    # Select first node
    query_name = "network_node/sys/node2"
    query = HypergraphCompartmentQuery(test_system, "query1", 0)
    query.set_lookup_name(query_name)
    node1 = list(query.execute())[0]
    # Select next node
    query_name = "network_node/sys/node1"
    query = HypergraphCompartmentQuery(test_system, "query2", 0)
    query.set_lookup_name(query_name)
    node2 = list(query.execute())[0]
    # Hypergraph edges
    edge = HypergraphEdge("test_edge", 0, test_system)
    # Connect
    edge.connect(node1, 1.0, 0, EnumRelationDirection.INWARDS)
    edge.connect(node2, 1.0, 0, EnumRelationDirection.OUTWARDS)
    for v in edge._subsets.values():
        assert v.parent is edge
    assert edge._subsets[node1.uid].endpoint is node1 and \
           edge._subsets[node1.uid].direction == EnumRelationDirection.INWARDS
    assert edge._subsets[node2.uid].endpoint is node2 and \
           edge._subsets[node2.uid].direction == EnumRelationDirection.OUTWARDS


def test_create_edge_with_query():
    _, test_system = SimpleTestFactory.create_4_nodes()
    # Add edge
    query = HypergraphEdgeDirectConnectNodes(test_system, "concept_edge", 0)
    query.add_endpoint_node("network_node/sys/node2")
    query.add_endpoint_node("network_node/sys/node1", EnumRelationDirection.INWARDS)
    edge = query.execute()
    assert len(edge.subset_elements) == 2
    # Tests
    query = HypergraphCompartmentQuery(test_system, "node_search", 0)
    query.set_lookup_name("network_node/sys/node1")
    node1: HypergraphNode = list(query.execute())[0]
    assert edge._subsets[node1.uid].endpoint is node1


def test_create_edge_with_query_functor():
    _, test_system = SimpleTestFactory.create_4_nodes()
    # Add edge
    edge = create_hyperedge("concept_edge", 0, test_system,
                            [("network_node/sys/node1", EnumRelationDirection.INWARDS),
                             ("network_node/sys/node2", EnumRelationDirection.OUTWARDS)])
    assert len(edge.subset_elements) == 2
    # Tests
    query = HypergraphCompartmentQuery(test_system, "node_search", 0)
    query.set_lookup_name("network_node/sys/node1")
    node1: HypergraphNode = list(query.execute())[0]
    assert edge._subsets[node1.uid].endpoint is node1