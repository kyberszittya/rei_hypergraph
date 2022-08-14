import asyncio
import numpy as np

from rei.foundations.hypergraph_traversal_strategies import HypergraphTraversal
from rei.hypergraph.homomorphism_functions import IndexHomomorphismGraphTensor
from rei.hypergraph.norm.norm_functions import SumNorm
from rei.tensor.tensor_representation import NumpyHypergraphTensorTransformer
from test.hypergraph.common_test_hypergraph_functions import simple_directed_graph_creation


def test_directed_edge_traversal_two_edge_with_homomorphism():
    _, _, n0, node_list, e = simple_directed_graph_creation()
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

def test_simple_directed_graph_representation():
    _, _, n0, node_list, e = simple_directed_graph_creation()
    tr = NumpyHypergraphTensorTransformer()
    asyncio.run(tr.execute(n0))
    # Weight
    assert np.all(tr.tensor_representation.W[0] == np.array([[0, 1, 0],
                                                             [0, 0, 0],
                                                             [0, 0, 0]]))
    assert np.all(tr.tensor_representation.W[1] == np.array([[0, 0, 1],
                                                             [0, 0, 0],
                                                             [0, 0, 0]]))
    # Incidences
    assert np.all(tr.tensor_representation.Io == np.array([[1, 0, 0],
                                                           [1, 0, 0]]))
    assert np.all(tr.tensor_representation.Ii == np.array([[0, 1, 0],
                                                           [0, 0, 1]]))
    # Derive incidence matrix
    assert np.all(tr.tensor_representation.Ii - tr.tensor_representation.Io == np.array([[-1, 1, 0],
                                                                                         [-1, 0, 1]]))
