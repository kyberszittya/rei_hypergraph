from rei.cognitive.channels.cognitive_dendrite import HypergraphTensorTransformation
from rei.cognitive.channels.cognitive_icons import TensorCognitiveIcon
from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from rei.cognitive.channels.channel_base_definitions import CognitiveChannel, CognitiveArbiter
from rei.cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge
from rei.cognitive.format.hypergraph.laplacian.graph_tensor_operations import graph_upper_bound_entropy_vector

import numpy as np
import numpy.testing

from rei.cognitive.format.hypergraph.operations.generative_operators import create_hyperedge, create_dir_edge
from rei.cognitive.messages.tensor_fragment import FragmentTensor


def create_fano_edge(sys: HypergraphNode, qualified_name: str, nodes: list[str]):
    sys.add_subset(
        create_hyperedge("e"+''.join(nodes), 0, sys,
                         [(qualified_name+x, EnumRelationDirection.UNDIRECTED) for x in nodes]), 0)


__FANO_ENTROPY: float = 11.09473750504809
__EXAMPLE_MULTITREE_ENTROPY = 12.89154140665565


def create_fano_graph():
    taxon = NetworkTaxonomy("test", 0)
    test_system = HypergraphNode("fano_graph", 0, domain=taxon)
    # Create nodes
    node_names = {"0", "1", "2", "3", "4", "5", "6"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
    # Create edges
    fano_pr = "test/fano_graph/"
    create_fano_edge(test_system, fano_pr, ["0", "1", "3"])
    create_fano_edge(test_system, fano_pr, ["1", "5", "6"])
    create_fano_edge(test_system, fano_pr, ["2", "3", "5"])
    create_fano_edge(test_system, fano_pr, ["1", "2", "4"])
    create_fano_edge(test_system, fano_pr, ["3", "4", "6"])
    create_fano_edge(test_system, fano_pr, ["0", "4", "5"])
    create_fano_edge(test_system, fano_pr, ["0", "2", "6"])
    return taxon, test_system


def create_multitree():
    taxon = NetworkTaxonomy("test", 0)
    test_system = HypergraphNode("multitree", 0, domain=taxon)
    # Create nodes
    node_names = {"0", "1", "2", "3", "4", "5", "6"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
    # Create edges
    tree_pr = "test/multitree/"
    create_dir_edge(test_system, tree_pr, ["4"], ["0", "1", "3"])
    create_dir_edge(test_system, tree_pr, ["2"], ["1", "5", "6"])
    create_dir_edge(test_system, tree_pr, ["1"], ["2", "3", "5"])
    create_dir_edge(test_system, tree_pr, ["6"], ["1", "2", "4"])
    create_dir_edge(test_system, tree_pr, ["1"], ["3", "4", "6"])
    create_dir_edge(test_system, tree_pr, ["3"], ["0", "4", "5"])
    create_dir_edge(test_system, tree_pr, ["1"], ["0", "2", "6"])
    return taxon, test_system


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


def setup_test_graph_elements(taxon, graph) -> FragmentTensor:
    sys = CognitiveArbiter(name="sys", timestamp=0, domain=taxon)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0, domain=taxon)
    ch = HypergraphTensorTransformation("dendrite1", 0, taxon, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    print()
    ch.encode([graph])
    fragment = view_icon.view()[0]
    return fragment


def test_basic_tensor_channel():
    """

    :return:
    """
    taxon, graph = create_fano_graph()
    fragment = setup_test_graph_elements(taxon, graph)
    assert fragment.V.shape == (7, 7, 7)
    assert np.all(np.sum(fragment.V, axis=0) + np.eye(7) == 1)
    # ASSERTION
    np.testing.assert_almost_equal(graph_upper_bound_entropy_vector(fragment.V)[0], __FANO_ENTROPY)


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
    assert np.all(np.sum(fragment.V, axis=0) + np.eye(7) == 1)
    entropy = graph_upper_bound_entropy_vector(fragment)
    # ASSERTION
    np.testing.assert_almost_equal(entropy[0], __FANO_ENTROPY)



def test_basic_tensor_channel_incidence():
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
    assert np.all(fragment.V @ fragment.I == 1)
    entropy = graph_upper_bound_entropy_vector(fragment)
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
    entropy = graph_upper_bound_entropy_vector(fragment.V)
    # ASSERTION
    np.testing.assert_almost_equal(entropy[0], __EXAMPLE_MULTITREE_ENTROPY)
