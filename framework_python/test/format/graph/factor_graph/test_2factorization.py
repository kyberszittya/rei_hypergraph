import asyncio

from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock
from rei.foundations.hierarchical_traversal_strategies import print_graph_hierarchy
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.factorization_operations import Factorization2Operation, MapFactorizationToFactorGraph


def create_simple_factor_graph_nodes():
    __clock = DummyClock()
    __factory = HypergraphFactory("factor_graph", __clock)
    _graph = __factory.generate_node("graph_sys")
    __node_names = [f"n{x}" for x in range(0,5)]
    nodes = []
    for i in __node_names:
        __n = __factory.generate_node(i, _graph)
        nodes.append(__n)
    return __factory, _graph, nodes, __node_names


def create_simple_factor_graph():
    __factory, _graph, nodes, __node_names = create_simple_factor_graph_nodes()
    edge = __factory.create_hyperedge(_graph, "e1")
    for i,s in enumerate(__node_names[1:]):
        edge.unary_connect(nodes[i+1], None, EnumRelationDirection.OUTWARDS)
    edge.unary_connect(nodes[0], None, EnumRelationDirection.INWARDS)
    return _graph


def factor_tuple(x):
    return [(x[0], x0) for x0 in x[1]]


def test_simple_edge_2factorization():
    _graph = create_simple_factor_graph()
    print()
    asyncio.run(print_graph_hierarchy(_graph))
    op = Factorization2Operation()
    l = asyncio.run(op.execute(_graph))
    mapping = MapFactorizationToFactorGraph(lambda x: factor_tuple(x))
    factorization = list(*asyncio.run(mapping.execute(l)))
    edgefactorset = {
        ('n0', 'n1'),
        ('n0', 'n2'),
        ('n0', 'n3'),
        ('n0', 'n4')
    }
    assert len(factorization) != 0
    res = set()
    for e in factorization:
        assert (e[0].endpoint.id_name, e[1].endpoint.id_name) in edgefactorset
        res.add(e)
    assert ('n0', 'n0') not in res
    assert ('n1', 'n0') not in res
    assert ('n2', 'n0') not in res


def test_simple_edge_2factorization_bidirectional():
    __factory, _graph, nodes, __node_names = create_simple_factor_graph_nodes()
    edge = __factory.create_hyperedge(_graph, "e1")
    for i,s in enumerate(__node_names[1:]):
        edge.unary_connect(nodes[i+1], None, EnumRelationDirection.BIDIRECTIONAL)
    edge.unary_connect(nodes[0], None, EnumRelationDirection.BIDIRECTIONAL)
    print()
    asyncio.run(print_graph_hierarchy(_graph))
    op = Factorization2Operation()
    l = asyncio.run(op.execute(_graph))
    mapping = MapFactorizationToFactorGraph(lambda x: factor_tuple(x))
    factorization = list(asyncio.run(mapping.execute(l)))
    edgefactorset = {
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    }
    assert len(factorization) != 0
    for e in factorization:
        i = e[0]
        assert (i[0].endpoint.id_name, i[1].endpoint.id_name) not in edgefactorset


def test_simple_edge_2factorization_pairing():
    """
    Test case to generate something similar to fully connected neural networks

    :return:
    """
    __factory, _graph, nodes, __node_names = create_simple_factor_graph_nodes()
    edge = __factory.create_hyperedge(_graph, "e1")
    for i,s in enumerate(__node_names[2:]):
        edge.unary_connect(nodes[i+2], None, EnumRelationDirection.OUTWARDS)
    edge.unary_connect(nodes[0], None, EnumRelationDirection.INWARDS)
    edge.unary_connect(nodes[1], None, EnumRelationDirection.INWARDS)
    print()
    asyncio.run(print_graph_hierarchy(_graph))
    op = Factorization2Operation()
    l = asyncio.run(op.execute(_graph))
    mapping = MapFactorizationToFactorGraph(lambda x: factor_tuple(x))
    factorization = list(asyncio.run(mapping.execute(l)))
    res = []
    for x in factorization:
        res.extend(x)
    edgefactorset = {
        ('0', '2'),
        ('0', '3'),
        ('0', '4'),
        ('1', '2'),
        ('1', '3'),
        ('1', '4')
    }
    assert len(factorization) != 0
    assert len(res) == 6
    res = set()
    for e in res:
        assert (e[0].endpoint.id_name, e[1].endpoint.id_name) in edgefactorset
        res.add(e)
    assert ('0', '1') not in res
    assert ('1', '0') not in res