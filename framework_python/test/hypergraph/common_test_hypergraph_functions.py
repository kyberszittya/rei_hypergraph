from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock

from test.hypergraph.common_hypergraph_test_literals import __TEST_HYPERGRAPH_FACTORY, __FIRST_NODE, __CNT_BASIC_ISOLATED_NODES, \
    __CNT_TRI_NODES
from rei.hypergraph.common_definitions import EnumRelationDirection


def dummy_node_test_creation():
    __clock = DummyClock()
    __factory = HypergraphFactory(__TEST_HYPERGRAPH_FACTORY,  __clock)
    return __clock, __factory


def test_single_hypergraph_node():
    __clock, __factory = dummy_node_test_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    assert n0.progenitor_qualified_name == '/'.join([__TEST_HYPERGRAPH_FACTORY, __FIRST_NODE])+".0"
    assert n0.uuid.hex() == "76cf5955e61190bbacd6e0b28f7ee2d095f083ea3945456952b646b1"
    assert n0.id_name == __FIRST_NODE


def test_2_isolated_nodes():
    __clock, __factory = dummy_node_test_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    for i in range(__CNT_BASIC_ISOLATED_NODES):
        __factory.generate_node(__FIRST_NODE+str(i), n0)
    assert n0.cnt_subelements == __CNT_BASIC_ISOLATED_NODES


def simple_graph_creation():
    __clock, __factory = dummy_node_test_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    node_list = []
    for i in range(__CNT_TRI_NODES):
        node_list.append(__factory.generate_node(__FIRST_NODE+str(i), n0))
    # A--B
    e1 = __factory.create_hyperedge(n0, "e12")
    e1.unary_connect(node_list[0], None, EnumRelationDirection.BIDIRECTIONAL)
    e1.unary_connect(node_list[1], None, EnumRelationDirection.BIDIRECTIONAL)
    # B--C
    e2 = __factory.create_hyperedge(n0, "e23")
    e2.unary_connect(node_list[0], None, EnumRelationDirection.BIDIRECTIONAL)
    e2.unary_connect(node_list[2], None, EnumRelationDirection.BIDIRECTIONAL)
    return __clock, __factory, n0, node_list, [e1, e2]


def simple_directed_graph_creation():
    __clock, __factory = dummy_node_test_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    node_list = []
    for i in range(__CNT_TRI_NODES):
        node_list.append(__factory.generate_node(__FIRST_NODE+str(i), n0))
    # A--B
    e1 = __factory.create_hyperedge(n0, "e12")
    e1.unary_connect(node_list[0], None, EnumRelationDirection.INWARDS)
    e1.unary_connect(node_list[1], None, EnumRelationDirection.OUTWARDS)
    # B--C
    e2 = __factory.create_hyperedge(n0, "e23")
    e2.unary_connect(node_list[0], None, EnumRelationDirection.INWARDS)
    e2.unary_connect(node_list[2], None, EnumRelationDirection.OUTWARDS)
    return __clock, __factory, n0, node_list, [e1, e2]
