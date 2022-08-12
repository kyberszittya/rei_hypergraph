import asyncio

from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.tensor.tensor_representation import IndexHomomorphismGraphTensor
from test.hypergraph.common_test_hypergraph_functions import dummy_node_test_creation


from common_hypergraph_test_literals import __FIRST_NODE, __CNT_TRI_NODES


def test_simple_graph_homomorphism():
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
    e2.unary_connect(node_list[1], None, EnumRelationDirection.BIDIRECTIONAL)
    # Homomorphism
    homomorphism = IndexHomomorphismGraphTensor(lambda x: x, lambda x: True)
    asyncio.run(homomorphism.execute(n0))
    # Node homomorphism
    assert homomorphism.dim(1) == node_list[0].uuid
    assert homomorphism.dim(2) == node_list[1].uuid
    assert homomorphism.dim(3) == node_list[2].uuid
    # Edge root
    assert homomorphism.depth(0) == e1.uuid
    assert homomorphism.depth(1) == e2.uuid
    assert homomorphism.edge(e1.uuid) == 0
    assert homomorphism.edge(e2.uuid) == 1
    # TODO: ignore root
