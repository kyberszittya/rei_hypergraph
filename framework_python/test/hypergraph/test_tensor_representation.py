import asyncio
import numpy as np

from rei.foundations.hypergraph_traversal_strategies import HypergraphTraversal
from rei.hypergraph.homomorphism_functions import IndexHomomorphismGraphTensor
from rei.hypergraph.norm.norm_functions import SumNorm
from rei.tensor.tensor_representation import NumpyHypergraphTensorTransformer
from test.hypergraph.common_test_hypergraph_functions import simple_graph_creation


def test_edge_traversal_homomorphism():
    _, _, n0, node_list, e = simple_graph_creation()
    res = []
    tr = HypergraphTraversal(lambda x: res.append(x), lambda x: True, SumNorm(), depth=1)
    asyncio.run(tr.execute(e[0]))
    assert len(res) == 4


def test_edge_traversal_one_edge():
    _, _, n0, node_list, e = simple_graph_creation()
    res = []
    tr = HypergraphTraversal(lambda x: res.append(x), lambda x: True, SumNorm(), depth=1)
    asyncio.run(tr.execute(e[0]))
    #assert len(res) == 4
    # 2-factorization
    # New edge
    assert res[0][0][0] == node_list[0].uuid
    assert res[0][0][1] == node_list[1].uuid
    assert res[0][0][2] == e[0].uuid
    assert res[0][0][3] == 1.0
    assert res[1][0][0] == node_list[1].uuid
    assert res[1][0][1] == node_list[0].uuid
    assert res[1][0][2] == e[0].uuid
    assert res[1][0][3] == 1.0


def test_edge_traversal_two_edge():
    _, _, n0, node_list, e = simple_graph_creation()
    res = []
    tr = HypergraphTraversal(lambda x: res.append(x), lambda x: True, SumNorm(), depth=1)
    asyncio.run(tr.execute(n0))
    #assert len(res) == 8
    # 2-factorization
    # New edge
    assert res[0][0][0] == node_list[0].uuid
    assert res[0][0][1] == node_list[1].uuid
    assert res[0][0][2] == e[0].uuid
    assert res[0][0][3] == 1.0
    assert res[1][0][0] == node_list[1].uuid
    assert res[1][0][1] == node_list[0].uuid
    assert res[1][0][2] == e[0].uuid
    assert res[1][0][3] == 1.0


def test_edge_traversal_two_edge_with_homomorphism():
    _, _, n0, node_list, e = simple_graph_creation()
    res = []
    homomorphism = IndexHomomorphismGraphTensor(True)
    asyncio.run(homomorphism.execute(n0))
    tr = HypergraphTraversal(lambda x: res.append(x), lambda x: True, SumNorm(), homomorphism, depth=1)
    asyncio.run(tr.execute(n0))
    # 2-factorization
    # New edge
    assert res[0][0][0] == 0
    assert res[0][0][1] == 1
    assert res[0][0][2] == 0
    assert res[0][0][3] == 1.0
    assert res[1][0][0] == 1
    assert res[1][0][1] == 0
    assert res[1][0][2] == 0
    assert res[1][0][3] == 1.0


def test_simple_graph_representation():
    _, _, n0, node_list, e = simple_graph_creation()
    tr = NumpyHypergraphTensorTransformer()
    asyncio.run(tr.execute(n0))
    # Weight
    assert np.all(tr.tensor_representation.W[0] == np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]]))
    assert np.all(tr.tensor_representation.W[1] == np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]]))
    # Incidences
    assert np.all(tr.tensor_representation.Io == np.array([[1, 1, 0],
                                                           [1, 0, 1]]))
    assert np.all(tr.tensor_representation.Ii == np.array([[1, 1, 0],
                                                           [1, 0, 1]]))



