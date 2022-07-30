from rei.cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode
from rei.cognitive.format.hypergraph.foundations.hypergraph_operators import \
    HypergraphCompartmentQuery, HypergraphDepthBidirectionalCompartmentQuery, HypergraphBidirectionalCompartmentQuery


__QUERY_NAME_BASE_HIERARCHY = "network_node/sys/node1/node2"


def test_retrieve_from_hierarchy():
    """
    Test simple hierarchy of hypergraph nodes
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2"}
    for n in node_names:
        n0 = HypergraphNode(n, 0)
        test_system.add_subset(n0, 0)
    query_name = "network_node/sys/node1"
    query = HypergraphCompartmentQuery(test_system, "query1", 0)
    query.set_lookup_name(query_name)
    res = query.execute()
    assert True in [i.progenitor_registry.qualified_name==query_name for i in res]


def test_retrieve_from_hierarchy_noelement():
    """
    Test simple hierarchy of hypergraph nodes
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2"}
    for n in node_names:
        n0 = HypergraphNode(n, 0)
        test_system.add_subset(n0, 0)
    query = HypergraphCompartmentQuery(test_system, "query1", 0)
    query_name = "network_node/sys/node9"
    query.set_lookup_name(query_name)
    res = query.execute()
    assert True not in [i.progenitor_registry.qualified_name==query_name for i in res]



def test_retrieve_from_hierarchy2():
    """
    Test simple hierarchy of hypergraphnodes
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
        for n1 in node_names:
            v1 = HypergraphNode(n1, 0)
            v0.add_subset(v1, 0)
    query_name = __QUERY_NAME_BASE_HIERARCHY
    query = HypergraphCompartmentQuery(test_system, "query1", 0)
    query.set_lookup_name(query_name)
    res = query.execute()
    res_list = list(res)
    assert True in [i.progenitor_registry.qualified_name==query_name for i in res_list]
    assert len(res_list)==1


def test_retrieve_from_hierarchy_bidirectional():
    """
    Test simple hierarchy of hypergraphnodes
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
        for n1 in node_names:
            v1 = HypergraphNode(n1, 0)
            v0.add_subset(v1, 0)
    query_name = __QUERY_NAME_BASE_HIERARCHY
    query = HypergraphCompartmentQuery(test_system, "query1", 0)
    query.set_lookup_name(query_name)
    res = list(query.execute())[0]
    query_bidirectional = HypergraphBidirectionalCompartmentQuery(res, "query1", 0)
    query_name2 = "network_node/sys/node2/node2"
    query_bidirectional.set_lookup_name(query_name2)
    res_2 = list(query_bidirectional.execute())
    assert len(res_2)==1
    assert res_2[0].progenitor_registry.qualified_name == query_name2


def test_retrieve_from_hierarchy_depth_bidirectional():
    """
    Test simple hierarchy of hypergraphnodes
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
        for n1 in node_names:
            v1 = HypergraphNode(n1, 0)
            v0.add_subset(v1, 0)
    query_name = __QUERY_NAME_BASE_HIERARCHY
    query = HypergraphCompartmentQuery(test_system, "query1", 0)
    query.set_lookup_name(query_name)
    res = list(query.execute())[0]
    query_depth_bidirectional = HypergraphDepthBidirectionalCompartmentQuery(res, "query1", 0)
    query_name2 = "network_node/sys/node1/node1"
    query_depth_bidirectional.set_lookup_name(query_name2)
    res_2 = list(query_depth_bidirectional.execute())
    assert len(res_2) == 1
    assert res_2[0].progenitor_registry.qualified_name == query_name2
    query_depth_bidirectional = HypergraphDepthBidirectionalCompartmentQuery(res, "query1", 0)
    query_name2 = "network_node/sys/node2"
    query_depth_bidirectional.set_lookup_name(query_name2)



