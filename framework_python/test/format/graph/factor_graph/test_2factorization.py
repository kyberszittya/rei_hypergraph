from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge
from rei.cognitive.format.hypergraph.foundations.hypergraph_operators import hypergraphedge_2factorization_tree


def test_simple_edge_2factorization():
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
    graph.add_subset(edge, 0)
    print()
    graph.print_hierarchy_tree()
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


def test_simple_edge_2factorization_bidirectional():
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


def test_simple_edge_2factorization_pairing():
    """
    Test case to generate something similar to fully connected neural networks

    :return:
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