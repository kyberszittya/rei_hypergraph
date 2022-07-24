from cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from cognitive.format.hypergraph.channels.tensor_channel import HypergraphTensorTransformation, CognitiveChannel, \
    TensorCognitiveIcon, CognitiveArbiter
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge
from cognitive.format.hypergraph.foundations.hypergraph_operators import \
    HypergraphCompartmentQuery, HypergraphDepthBidirectionalCompartmentQuery, \
    HypergraphBidirectionalCompartmentQuery, HypergraphEdgeDirectConnectNodes, \
    create_hyperedge, retrieve_part_hypergraph_node, create_dir_edge
from cognitive.format.hypergraph.laplacian.graph_tensor_operations import graph_lower_bound_entropy_vector, \
    graph_upper_bound_entropy_vector, laplacian_calc_vector


def create_fano_edge(sys: HypergraphNode, qualified_name: str, nodes: list[str]):
    sys.add_subset(
        create_hyperedge("e"+''.join(nodes), 0, sys,
                         [(qualified_name+x, EnumRelationDirection.UNDIRECTED) for x in nodes]), 0)


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
    for set in fano_graph.subset_elements:
        if isinstance(set, HypergraphNode):
            assert int(set.progenitor_registry.name) in range(0, 7)
        elif isinstance(set, HypergraphEdge):
            set.print_elements()


def test_basic_tensor_channel():
    """

    :return:
    """
    taxon, graph = create_fano_graph()
    sys = CognitiveArbiter(name="sys", timestamp=0, domain=taxon)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0, domain=taxon)
    ch = HypergraphTensorTransformation("dendrite1", 0, taxon, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    print()
    tensor = ch.encode([graph])
    print(tensor)
    import numpy as np
    assert tensor.shape == (7,7,7)
    assert np.all(np.sum(tensor, axis=0) + np.eye(7)==1)
    assert graph_upper_bound_entropy_vector(tensor) == 2.807354922057604


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
    tensor = ch.encode([graph])
    import numpy as np
    assert tensor.shape == (7,7,7)
    assert np.all(np.sum(tensor, axis=0) + np.eye(7)==1)
    assert graph_upper_bound_entropy_vector(tensor) == 2.807354922057604


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
    tensor = ch.encode([graph])
    print(tensor)
