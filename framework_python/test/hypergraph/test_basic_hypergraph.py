import asyncio

from rei.foundations.hierarchical_traversal_strategies import BreadthFirstHierarchicalTraversal
from rei.hypergraph.base_elements import HypergraphRelation
from rei.hypergraph.common_definitions import EnumRelationDirection

from test.hypergraph.common_hypergraph_test_literals import __FIRST_NODE, __CNT_BASIC_NODES, __SINGLE_EDGE_NAME
from test.hypergraph.common_test_hypergraph_functions import dummy_node_test_factory_creation


def test_connect_nodes():
    __clock, __factory = dummy_node_test_factory_creation()
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
    trav = BreadthFirstHierarchicalTraversal(lambda x: names_list.append(x.id_name),
                                          lambda x: isinstance(x, HypergraphRelation))
    asyncio.get_event_loop().run_until_complete(trav.execute(e))
    assert '_'.join(names_list) == '_'.join(["reledge.node0."+'0', "reledge.node1."+'0'])
    induced_subset = set(map(lambda x: x.id_name, e.induced_subset))
    assert len(induced_subset) == 2
    for i in range(2):
        assert __FIRST_NODE+str(i) in induced_subset


__V0_FIRST_VALUE = 1.0
__V1_FIRST_VALUE = 2.0
__V0_2ND_VALUE = 10.0
__V0_3RD_VALUE = -4.0
__V1_2ND_VALUE = -256.7
__VAL0_NAME = "val0"
__VAL1_NAME = "val1"


def test_connect_nodes_with_values():
    __clock, __factory = dummy_node_test_factory_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    node_list = []
    for i in range(__CNT_BASIC_NODES):
        node_list.append(__factory.generate_node(__FIRST_NODE+str(i), n0))
    e = __factory.create_hyperedge(n0, __SINGLE_EDGE_NAME)
    assert e.id_name == "edge"
    # Values
    v0 = __factory.create_value(n0, __VAL0_NAME, [__V0_FIRST_VALUE])
    v1 = __factory.create_value(n0, __VAL1_NAME, [__V1_FIRST_VALUE])
    # Connections
    e.unary_connect(node_list[0], v0, EnumRelationDirection.BIDIRECTIONAL)
    e.unary_connect(node_list[1], v1, EnumRelationDirection.BIDIRECTIONAL)
    rels = (list(e.get_subelements(lambda x: isinstance(x, HypergraphRelation))))
    names_list = []
    trav = BreadthFirstHierarchicalTraversal(lambda x: names_list.append(x.id_name),
                                             lambda x: isinstance(x, HypergraphRelation))
    asyncio.get_event_loop().run_until_complete(trav.execute(e))
    assert '_'.join(names_list) == '_'.join(["reledge.node0."+'0', "reledge.node1."+'0'])
    induced_subset = set(map(lambda x: x.id_name, e.induced_subset))
    assert len(induced_subset) == 2
    for i in range(2):
        assert __FIRST_NODE+str(i) in induced_subset
    # Check values
    assert rels[0].weight[0] == __V0_FIRST_VALUE
    assert rels[1].weight[0] == __V1_FIRST_VALUE
    # Change value
    v0.update_value(0, __V0_2ND_VALUE)
    assert v0[0] == __V0_2ND_VALUE
    assert rels[0].weight[0] == __V0_2ND_VALUE
    v0[0] = __V0_3RD_VALUE
    assert rels[0].weight[0] == __V0_3RD_VALUE
    v1[0] = __V1_2ND_VALUE
    assert rels[1].weight[0] == __V1_2ND_VALUE
    # Ensure values have the correct parents
    assert v0.parent is n0
    assert v1.parent is n0
    # Retrieve values from node
    val_list = list(n0.sub_values)
    assert len(val_list) == 2
    assert '.'.join(map(lambda x: x.id_name, val_list)) == ".".join([__VAL0_NAME, __VAL1_NAME])
    # Retrieve specific value
    vals = list(n0.get_element_by_id_name(__VAL0_NAME))
    assert len(vals) == 1
    assert vals[0][0] == __V0_3RD_VALUE


