import asyncio
import numpy as np

from rei.foundations.hypergraph_traversal_strategies import HypergraphTraversal
from rei.hypergraph.norm_functions import sum_norm
from rei.tensor.tensor_representation import NumpyHypergraphTensorTransformer
from test.hypergraph.common_test_hypergraph_functions import simple_graph_creation


def test_edge_traversal():
    _, _, n0, node_list, e = simple_graph_creation()
    tr = HypergraphTraversal(lambda x: x, lambda x: True, sum_norm)
    asyncio.run(tr.execute(e[0]))


def test_simple_graph_representation():
    _, _, n0, node_list, e = simple_graph_creation()
    tr = NumpyHypergraphTensorTransformer()
    asyncio.run(tr.execute(n0))
    print(tr.tensor_representation.W)
    assert np.all(tr.tensor_representation.Io == np.array([[1, 1, 0], [1, 0, 1]]))
    assert np.all(tr.tensor_representation.Ii == np.array([[1, 1, 0], [1, 0, 1]]))

