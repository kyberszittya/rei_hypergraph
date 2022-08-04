from rei.cognitive.channels.cognitive_dendrite import HypergraphTensorTransformation
from rei.cognitive.channels.cognitive_icons import TensorCognitiveIcon
from rei.cognitive.channels.channel_base_definitions import CognitiveChannel, CognitiveArbiter
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge
from rei.cognitive.format.hypergraph.laplacian.graph_tensor_operations import graph_upper_bound_entropy_vector, \
    laplacian_calc_vector

import numpy as np
import numpy.testing

from test.common.basic_graph_creation_functions import create_fano_graph, create_multitree, setup_test_graph_elements, \
    create_simple_tree

__FANO_ENTROPY: float = 4.39231742277876
__EXAMPLE_MULTITREE_ENTROPY = 11.094737505048094


def test_fano_graph_basic():
    """
    Test the creation of the Fano-graph
    :return:
    """
    _, fano_graph = create_fano_graph()
    assert len(fano_graph._subsets) == 14
    print()
    for subset in fano_graph.subset_elements:
        if isinstance(subset, HypergraphNode):
            assert int(subset.progenitor_registry.name) in range(0, 7)
        elif isinstance(subset, HypergraphEdge):
            subset.print_elements()
            assert len(list(subset.subrelations)) == 3
            for subrel in subset.subrelations:
                # TODO: Assert valid connections
                pass
                #print(subrel)


def test_basic_tensor_channel():
    """

    :return:
    """
    taxon, graph = create_fano_graph()
    fragment = setup_test_graph_elements(taxon, graph)
    assert fragment.V.shape == (7, 7, 7)
    assert np.all(np.sum(fragment.V, axis=2) + np.eye(7) == 1)
    # ASSERTION
    np.testing.assert_almost_equal(graph_upper_bound_entropy_vector(fragment.V.T)[0], __FANO_ENTROPY)


def test_basic_tensor_channel_incidence_format():
    """

    :return:
    """
    taxon, graph = create_fano_graph()
    fragment = setup_test_graph_elements(taxon, graph)
    assert fragment.V.shape == (7, 7, 7)
    D_m, L, deg = laplacian_calc_vector(fragment.V.T)
    assert deg == 42.0
    d = np.sum(D_m, axis=0)
    assert d[0, 0] == 6
    assert d[1, 1] == 6
    assert d[2, 2] == 6
    assert d[3, 3] == 6
    assert d[4, 4] == 6
    assert d[5, 5] == 6
    assert d[6, 6] == 6
    # Check Laplacian
    L_sigma = np.sum(L, axis=0)
    assert L_sigma[0, 0] == 6
    assert L_sigma[1, 1] == 6
    assert L_sigma[2, 2] == 6
    assert L_sigma[3, 3] == 6
    assert L_sigma[4, 4] == 6
    assert L_sigma[5, 5] == 6
    assert L_sigma[6, 6] == 6
    assert L_sigma[0, 6] == -1
    # Also check is this computes
    assert np.all(np.sum(fragment.V.T, axis=0) + np.eye(7) == 1)


def test_basic_tensor_channel_2():
    """

    :return:
    """
    _, graph = create_fano_graph()
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
    entropy = graph_upper_bound_entropy_vector(fragment.V.T)
    # ASSERTION
    np.testing.assert_almost_equal(entropy[0], __FANO_ENTROPY)


def test_basic_tensor_channel_3():
    """

    :return:
    """
    _, graph = create_multitree()
    sys = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, sys.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    print()
    ch.encode([graph])
    fragment = view_icon.view()[0]
    entropy = graph_upper_bound_entropy_vector(fragment.V.T)
    # ASSERTION
    np.testing.assert_almost_equal(entropy[0], __EXAMPLE_MULTITREE_ENTROPY)


def test_basic_simpletree():
    """

    :return:
    """
    taxon, graph = create_simple_tree()
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
    entropy = graph_upper_bound_entropy_vector(fragment.V.T)
    print(entropy)
