import asyncio

from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock
from rei.foundations.hierarchical_traversal_strategies import print_graph_hierarchy
from rei.hypergraph.common_definitions import EnumRelationDirection


def create_simple_factor_graph():
    __clock = DummyClock()
    __factory = HypergraphFactory("factor_graph", __clock)
    _graph = __factory.generate_node("graph_sys")
    __node_names = [f"n{x}" for x in range(0,5)]
    nodes = []
    for i in __node_names:
        __n = __factory.generate_node(i, _graph)
        nodes.append(__n)
    edge = __factory.create_hyperedge(_graph, "e1")
    for i,s in enumerate(__node_names[1:]):
        edge.unary_connect(nodes[i+1], None, EnumRelationDirection.OUTWARDS)
    edge.unary_connect(nodes[0], None, EnumRelationDirection.INWARDS)
    return _graph


def test_simple_edge_2factorization():
    _graph = create_simple_factor_graph()
    print()
    asyncio.run(print_graph_hierarchy(_graph))

    """
    factorization = hypergraphedge_2factorization_tree(edge)
    edgefactorset = {
        ('0', '1'),
        ('0', '2'),
        ('0', '3'),
        ('0', '4')
    }
    assert not factorization.empty()
    res = set()
    while not factorization.empty():
        e = factorization.get()
        assert ((e[0].endpoint.id_name, e[1].endpoint.id_name) in edgefactorset)
        res.add(e)
    assert ('0', '0') not in res
    assert ('1', '0') not in res
    assert ('2', '0') not in res
    """


def test_simple_edge_2factorization_bidirectional():
    _graph = create_simple_factor_graph()
    """
    graph = HypergraphNode("graph_sys", 0)
    node_names = [str(x) for x in range(0,5)]
    nodes = []
    for i in node_names:
        n = HypergraphNode(i, 0)
        nodes.append(n)
        graph.add_subset(n, 0)
    edge = HypergraphEdge("e1", 0, graph)
    for i,s in enumerate(node_names[0:]):
        edge.connect(nodes[i], 1.0, 0, EnumRelationDirection.UNDIRECTED)
    edge.connect(nodes[0], 1.0, 0, EnumRelationDirection.UNDIRECTED)
    graph.add_subset(edge, 0)
    print()
    graph.print_hierarchy_tree()
    factorization = hypergraphedge_2factorization_tree(edge)
    edgefactorset = {
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    }
    assert not factorization.empty()
    while not factorization.empty():
        e = factorization.get()
        assert (e[0].endpoint.id_name, e[1].endpoint.id_name) not in edgefactorset
    """


def test_simple_edge_2factorization_pairing():
    """
    Test case to generate something similar to fully connected neural networks

    :return:
    """
    _graph = create_simple_factor_graph()
    """
    graph = HypergraphNode("graph_sys", 0)
    node_names = [str(x) for x in range(0,5)]
    nodes = []
    for i in node_names:
        n = HypergraphNode(i, 0)
        nodes.append(n)
        graph.add_subset(n, 0)
    edge = HypergraphEdge("e1", 0, graph)
    for i,s in enumerate(node_names[0:]):
        edge.connect(nodes[i], 1.0, 0, EnumRelationDirection.OUTWARDS)
    edge.connect(nodes[0], 1.0, 0, EnumRelationDirection.INWARDS)
    edge.connect(nodes[1], 1.0, 0, EnumRelationDirection.INWARDS)
    graph.add_subset(edge, 0)
    print()
    graph.print_hierarchy_tree()
    factorization = hypergraphedge_2factorization_tree(edge)
    edgefactorset = {
        ('0', '2'),
        ('0', '3'),
        ('0', '4'),
        ('1', '2'),
        ('1', '3'),
        ('1', '4')
    }
    assert not factorization.empty()
    res = set()
    while not factorization.empty():
        e = factorization.get()
        assert (e[0].endpoint.id_name, e[1].endpoint.id_name) in edgefactorset
        res.add(e)
    assert ('0', '1') not in res
    assert ('1', '0') not in res
    """