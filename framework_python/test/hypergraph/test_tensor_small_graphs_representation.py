import asyncio
import numpy as np

from rei.foundations.clock import DummyClock
from rei.hypergraph.sample_graphs.fano_graph import create_fano_graph
from rei.tensor.tensor_representation import NumpyHypergraphTensorTransformer
from test.hypergraph.common_test_hypergraph_functions import dummy_node_test_factory_creation


__FIRST_NODE = "taxon"


def test_undirected_fano_graph():
    __clock, __factory = dummy_node_test_factory_creation()
    __n0 = __factory.generate_node(__FIRST_NODE)
    __node_list = __factory.generate_list_nodes([str(x) for x in range(7)], __n0)
    # Check whether anyhow the UUIDs are not equal
    __uuid_set = set()
    for n in __node_list:
        assert n.uuid not in __uuid_set
        __uuid_set.add(n.uuid)
    # Connect the set of nodes
    __edges = [__factory.connect_nodes(__n0, "e012", [__node_list[0], __node_list[1], __node_list[2]]),
             __factory.connect_nodes(__n0, "e234", [__node_list[2], __node_list[3], __node_list[4]]),
             __factory.connect_nodes(__n0, "e146", [__node_list[1], __node_list[4], __node_list[6]]),
             __factory.connect_nodes(__n0, "e036", [__node_list[0], __node_list[3], __node_list[6]]),
             __factory.connect_nodes(__n0, "e256", [__node_list[2], __node_list[5], __node_list[6]]),
             __factory.connect_nodes(__n0, "e135", [__node_list[1], __node_list[3], __node_list[5]]),
             __factory.connect_nodes(__n0, "e045", [__node_list[0], __node_list[4], __node_list[5]])]
    # Ensure there are 7 edges
    assert len(list(__n0.sub_edges)) == 7
    # Ensure each edge have 3 sub-relations
    for e in __edges:
        assert len(list(e.sub_relations)) == 3
    # Transform to tensor representation
    tr = NumpyHypergraphTensorTransformer()
    asyncio.run(tr.execute(__n0))
    # Ensure the adjacency matrix is as it is
    assert (np.all(np.sum(tr.tensor_representation.W, axis=0) + np.eye(7) == np.ones(shape=(7,7))))
    # Check structure (adjacency)
    # E-012
    assert np.all(tr.tensor_representation.W[0] == np.array([
        [0, 1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]))
    # E-234
    assert np.all(tr.tensor_representation.W[1] == np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]))
    # E-146
    assert np.all(tr.tensor_representation.W[2] == np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 0, 0]
    ]))
    # E-036
    assert np.all(tr.tensor_representation.W[3] == np.array([
        [0, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0]
    ]))
    # E-256
    assert np.all(tr.tensor_representation.W[4] == np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0]
    ]))
    # E-135
    assert np.all(tr.tensor_representation.W[5] == np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]))
    # E-045
    assert np.all(tr.tensor_representation.W[6] == np.array([
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]))
    # Edge structure check
    # Check incidence
    assert np.all(tr.tensor_representation.Io == np.array([
        [1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 1, 0]
    ]))
    assert np.all(tr.tensor_representation.Ii == np.array([
        [1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 1, 0]
    ]))
    assert np.all(tr.tensor_representation.Ii == tr.tensor_representation.Io)


def test_undirected_fano_graph_degree_matrix():
    _, __n0, __node_list, __edges = create_fano_graph("fano_test", DummyClock())
    tr = NumpyHypergraphTensorTransformer()
    asyncio.run(tr.execute(__n0))
    assert np.all(np.sum(tr.tensor_representation.Io, axis=1) == np.array([3, 3, 3, 3, 3, 3, 3]))
    assert np.all(np.sum(tr.tensor_representation.Ii, axis=1) == np.array([3, 3, 3, 3, 3, 3, 3]))
    # Check degree matrix calculations
    assert np.all(tr.tensor_representation.deg == np.array([3, 3, 3, 3, 3, 3, 3]))
    assert np.all(tr.tensor_representation.D == np.eye(7) * 3.0)
    assert tr.tensor_representation.total_deg == 21
