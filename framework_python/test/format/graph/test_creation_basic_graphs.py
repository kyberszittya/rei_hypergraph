from _pytest.outcomes import fail


import numpy as np
import numpy.testing

from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge
from rei.hypergraph.common_definitions import EnumRelationDirection
from test.common.basic_graph_creation_functions import create_fano_graph, create_multitree, create_simple_tree

__FANO_ENTROPY: float = 8.605303928306439
__EXAMPLE_MULTITREE_ENTROPY = 9.73238460346960


def test_fano_graph_basic():
    """
    Test the creation of the Fano-graph
    :return:
    """
    _, _, fano_graph = create_fano_graph()
    assert fano_graph.cnt_subelements == 14
    print()
    # Result sets
    expected_edge_connections = {
        "e013": "013",
        "e156": "156",
        "e235": "235",
        "e124": "124",
        "e346": "346",
        "e045": "045",
        "e026": "026"
    }
    # Iterate through all elements
    for node in fano_graph.sub_nodes:
        print(node)
    for e in fano_graph.sub_edges:
        #e.print_elements()
        assert e.cnt_subelements == 3
        relation_id = []
        for subrel in e.sub_relations:
            if subrel.direction != EnumRelationDirection.BIDIRECTIONAL:
                fail("Not undirected")
            relation_id.append(subrel.endpoint.id_name)
        assert expected_edge_connections[e.id_name] == ''.join(relation_id)


def test_basic_tensor_channel():
    """

    :return:
    """
    _, _, graph = create_fano_graph()
    """
    fragment = setup_test_graph_elements(taxon, graph)
    assert fragment.V.shape == (7, 7, 7)
    assert np.all(np.sum(fragment.V, axis=2) + np.eye(7) == 1)
    # ASSERTION
    np.testing.assert_almost_equal(entropy_normalized_laplacian(fragment), __FANO_ENTROPY)
    """


def test_tensor_fragment_properties():
    _, _, graph = create_fano_graph()
    """
    fragment = setup_test_graph_elements(taxon, graph)
    assert fragment.V.shape == (7, 7, 7)
    assert np.all(np.sum(fragment.V, axis=2) + np.eye(7) == 1)
    # Test properties
    D_proj = np.sum(fragment.D, axis=0)
    assert D_proj[0, 0] == D_proj[1, 1] == D_proj[2, 2] == D_proj[3, 3] == \
           D_proj[4, 4] == D_proj[5, 5] == D_proj[6, 6] == 12
    assert np.all(np.abs(np.sum(fragment.L, axis=0) - np.eye(7) * 11) == 1)
    """


def test_basic_tensor_channel_incidence_format():
    """

    :return:
    """
    _, _, graph = create_fano_graph()
    """
    fragment = setup_test_graph_elements(taxon, graph)
    assert fragment.V.shape == (7, 7, 7)
    L = fragment.L
    # Check Laplacian
    L_sigma = np.sum(L, axis=0)
    assert L_sigma[0, 0] == 12
    assert L_sigma[1, 1] == 12
    assert L_sigma[2, 2] == 12
    assert L_sigma[3, 3] == 12
    assert L_sigma[4, 4] == 12
    assert L_sigma[5, 5] == 12
    assert L_sigma[6, 6] == 12
    assert L_sigma[0, 6] == -1
    # Also check is this computes
    assert np.all(np.sum(fragment.V.T, axis=0) + np.eye(7) == 1)
    """


def test_basic_tensor_channel_2():
    """

    :return:
    """
    _, _, graph = create_fano_graph()
    """
    sys = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, sys.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    print()
    ch.encode([graph])    
    fragment = view_icon.view()[0]
    assert fragment.V.shape == (7, 7, 7)
    assert np.all(np.sum(fragment.V, axis=2) + np.eye(7) == 1)
    entropy = entropy_normalized_laplacian(fragment)
    # ASSERTION
    np.testing.assert_almost_equal(entropy, __FANO_ENTROPY)
    """


def test_basic_tensor_channel_3():
    """

    :return:
    """
    _, _, graph = create_multitree()
    """
    sys = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, sys.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    print()
    ch.encode([graph])
    fragment = view_icon.view()[0]
    entropy = entropy_normalized_laplacian(fragment)
    # ASSERTION
    np.testing.assert_almost_equal(entropy, __EXAMPLE_MULTITREE_ENTROPY)
    """


def test_basic_simpletree():
    """

    :return:
    """
    _, _, graph = create_simple_tree()
    """
    fragment = setup_test_graph_elements(taxon, graph)
    assert fragment.V.T[0, 0, 0] == 0.0
    assert fragment.V.T[0, 0, 1] == 1.0
    assert fragment.V.T[0, 0, 0] == 0.0
    assert fragment.V.T[1, 0, 2] == 1.0
    assert fragment.V.T[1, 0, 1] == 0.0
    assert fragment.V.T[1, 1, 1] == 0.0
    # Incidence matrix test
    assert fragment.I[0, 0] == -1.0
    assert fragment.I[0, 1] == -1.0
    assert fragment.I[1, 0] == 1.0
    assert fragment.I[1, 1] == 0.0
    assert fragment.I[2, 0] == 0.0
    assert fragment.I[2, 1] == 1.0
    # Entropy
    entropy = entropy_normalized_laplacian(fragment)
    assert entropy == 2.0
    """
