import asyncio

from rei.foundations.query.search_elements import QuerySearchSubElement, QuerySearchElement
from test.hypergraph.common_test_hypergraph_functions import dummy_node_test_factory_creation

__QUERY_NAME_BASE_HIERARCHY = "network_node/sys/node1/node2"


def test_retrieve_from_hierarchy():
    """
    Test simple hierarchy of hypergraph nodes
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", taxon)
    node_names = {"node1", "node2"}

    for n in node_names:
        n0 = __factory.generate_node(n, test_system)
        #test_system.add_subset(n0, 0)
    query_name = "network_node/sys/node1"
    # Query search
    query = QuerySearchSubElement()
    query.query_def = query_name
    asyncio.get_event_loop().run_until_complete(query.execute(taxon))
    assert True in [i.qualified_name == query_name for i in query.query_result]


def test_retrieve_from_hierarchy_noelement():
    """
    Test simple hierarchy of hypergraph nodes
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", taxon)
    node_names = {"node1", "node2"}

    for n in node_names:
        n0 = __factory.generate_node(n, test_system)
        #test_system.add_subset(n0, 0)
    # Query search
    query = QuerySearchSubElement()
    query_name = "network_node/sys/node9"
    query.query_def = query_name
    asyncio.get_event_loop().run_until_complete(query.execute(taxon))
    assert True not in [i.qualified_name==query_name for i in query.query_result]


def test_retrieve_from_hierarchy2():
    """
    Test simple hierarchy of hypergraphnodes
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", taxon)
    node_names = {"node1", "node2"}

    for n0 in node_names:
        v0 = __factory.generate_node(n0, test_system)
        #test_system.add_subset(v0, 0)
        for n1 in node_names:
            v1 = __factory.generate_node(n1, v0)
            #v0.add_subset(v1, 0)
    query_name = __QUERY_NAME_BASE_HIERARCHY
    query = QuerySearchSubElement()
    query.query_def = query_name
    asyncio.get_event_loop().run_until_complete(query.execute(taxon))
    assert True in [i.qualified_name == query_name for i in query.query_result]
    assert len(query.query_result) == 1



def test_retrieve_from_hierarchy_cached_element():
    """
    Test simple hierarchy of hypergraphnodes
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", taxon)
    node_names = {"node1", "node2"}

    for n0 in node_names:
        v0 = __factory.generate_node(n0, test_system)
        #test_system.add_subset(v0, 0)
        for n1 in node_names:
            v1 = __factory.generate_node(n1, v0)
            #v0.add_subset(v1, 0)
    query_name = __QUERY_NAME_BASE_HIERARCHY
    # Query setup
    query = QuerySearchSubElement()
    query.query_def = query_name
    asyncio.get_event_loop().run_until_complete(query.execute(taxon))
    assert True in [i.qualified_name == query_name for i in query.query_result]
    assert len(query.query_result) == 1
    asyncio.get_event_loop().run_until_complete(query.execute(taxon))
    assert True in [i.qualified_name == query_name for i in query.query_result]
    assert len(query.query_result) == 1


def test_retrieve_from_hierarchy_bidirectional():
    """
    Test simple hierarchy of hypergraphnodes
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", taxon)
    node_names = {"node1", "node2"}
    nodes = []
    for n0 in node_names:
        v0 = __factory.generate_node(n0, test_system)
        nodes.append(v0)
        for n1 in node_names:
            v1 = __factory.generate_node(n1, v0)
    query_name = __QUERY_NAME_BASE_HIERARCHY
    query = QuerySearchElement()
    query.query_def = query_name
    asyncio.get_event_loop().run_until_complete(query.execute(nodes[0]))
    res = query.query_result
    assert len(res) == 1
    assert res[0].qualified_name == query_name
    query_name2 = "network_node/sys/node2/node2"
    query.query_def = query_name2
    asyncio.get_event_loop().run_until_complete(query.execute(nodes[0]))
    res_2 = query.query_result
    assert len(res_2) == 1
    assert res_2[0].qualified_name == query_name2


def test_retrieve_from_hierarchy_depth_bidirectional():
    """
    Test simple hierarchy of hypergraphnodes
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", taxon)
    node_names = {"node1", "node2"}
    nodes = []
    for n0 in node_names:
        v0 = __factory.generate_node(n0, test_system)
        nodes.append(v0)
        for n1 in node_names:
            v1 = __factory.generate_node(n1, v0)
    query_name = __QUERY_NAME_BASE_HIERARCHY
    query = QuerySearchSubElement()
    query.query_def = query_name
    asyncio.get_event_loop().run_until_complete(query.execute(nodes[0]))
    res_parent = query.query_result[0]
    query_depth_bidirectional = QuerySearchElement()
    query_name2 = "network_node/sys/node1/node1"
    query_depth_bidirectional.query_def = query_name2
    asyncio.get_event_loop().run_until_complete(query_depth_bidirectional.execute(res_parent))
    res_2 = query_depth_bidirectional.query_result
    assert len(res_2) == 1
    assert res_2[0].qualified_name == query_name2
    query_name2 = "network_node/sys/node2"
    query_depth_bidirectional.query_def = query_name2
