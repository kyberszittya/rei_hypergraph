import asyncio

from rei.tensor.tensor_representation import IndexHomomorphismGraphTensor
from test.hypergraph.common_test_hypergraph_functions import simple_graph_creation


def test_simple_graph_homomorphism():
    _, _, n0, node_list, e = simple_graph_creation()
    # Homomorphism
    homomorphism = IndexHomomorphismGraphTensor()
    asyncio.run(homomorphism.execute(n0))
    # Node homomorphism
    assert homomorphism.dim(1) == node_list[0].uuid
    assert homomorphism.dim(2) == node_list[1].uuid
    assert homomorphism.dim(3) == node_list[2].uuid
    # Edge root
    assert homomorphism.depth(0) == e[0].uuid
    assert homomorphism.depth(1) == e[1].uuid
    assert homomorphism.edge(e[0].uuid) == 0
    assert homomorphism.edge(e[1].uuid) == 1


def test_simple_graph_homomorphism_ignored_root():
    _, _, n0, node_list, e = simple_graph_creation()
    # Homomorphism
    homomorphism = IndexHomomorphismGraphTensor(True)
    asyncio.run(homomorphism.execute(n0))
    # Node homomorphism
    assert homomorphism.dim(0) == node_list[0].uuid
    assert homomorphism.dim(1) == node_list[1].uuid
    assert homomorphism.dim(2) == node_list[2].uuid
    # Edge root
    assert homomorphism.depth(0) == e[0].uuid
    assert homomorphism.depth(1) == e[1].uuid
    assert homomorphism.edge(e[0].uuid) == 0
    assert homomorphism.edge(e[1].uuid) == 1
