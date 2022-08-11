import asyncio

from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock
from rei.hypergraph.base_elements import HypergraphRelation
from rei.hypergraph.common_definitions import EnumRelationDirection

__TEST_HYPERGRAPH_FACTORY = "test.hypergraphnode"
__FIRST_NODE = "node"
__CNT_BASIC_ISOLATED_NODES = 2
__CNT_BASIC_NODES = 4
__SINGLE_EDGE_NAME = "edge"


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


def test_connect_nodes():
    __clock, __factory = dummy_node_test_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    node_list = []
    for i in range(__CNT_BASIC_NODES):
        node_list.append(__factory.generate_node(__FIRST_NODE+str(i), n0))
    e = __factory.create_hyperedge(n0, __SINGLE_EDGE_NAME)
    assert e.id_name == "edge"
    e.unary_connect(node_list[0], None, EnumRelationDirection.BIDIRECTIONAL)
    e.unary_connect(node_list[1], None, EnumRelationDirection.BIDIRECTIONAL)
    rels = (list(e.get_subelements(lambda x: isinstance(x, HypergraphRelation))))
    assert len(rels) == 2
    names_list = []
    asyncio.get_event_loop().run_until_complete(e.breadth_visit_children(
        lambda x: names_list.append(x.id_name), lambda x: isinstance(x, HypergraphRelation)))
    assert '_'.join(names_list) == '_'.join(["reledge.node0."+'0', "reledge.node1."+'0'])
    induced_subset = set(map(lambda x: x.id_name, e.induced_subset))
    assert len(induced_subset) == 2
    for i in range(2):
        assert __FIRST_NODE+str(i) in induced_subset


def test_connect_nodes_with_values():
    __clock, __factory = dummy_node_test_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    node_list = []
    for i in range(__CNT_BASIC_NODES):
        node_list.append(__factory.generate_node(__FIRST_NODE+str(i), n0))
    e = __factory.create_hyperedge(n0, __SINGLE_EDGE_NAME)
    assert e.id_name == "edge"
    # Values
    v0 = __factory.create_value(n0, "val0", [1.0])
    v1 = __factory.create_value(n0, "val1", [2.0])
    # Connections
    e.unary_connect(node_list[0], v0, EnumRelationDirection.BIDIRECTIONAL)
    e.unary_connect(node_list[1], v1, EnumRelationDirection.BIDIRECTIONAL)
    rels = (list(e.get_subelements(lambda x: isinstance(x, HypergraphRelation))))
    assert len(rels) == 2
    names_list = []
    asyncio.get_event_loop().run_until_complete(e.breadth_visit_children(
        lambda x: names_list.append(x.id_name), lambda x: isinstance(x, HypergraphRelation)))
    assert '_'.join(names_list) == '_'.join(["reledge.node0."+'0', "reledge.node1."+'0'])
    induced_subset = set(map(lambda x: x.id_name, e.induced_subset))
    assert len(induced_subset) == 2
    for i in range(2):
        assert __FIRST_NODE+str(i) in induced_subset
    # Check values
    assert rels[0].weight[0] == 1.0
    assert rels[1].weight[0] == 2.0
    # Change value
    v1.update_value(0, 10.0)
    print(rels[0].weight[0])
