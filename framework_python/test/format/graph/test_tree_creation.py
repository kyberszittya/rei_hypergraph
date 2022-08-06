from rei.cognitive.channels.cognitive_dendrite import HypergraphTensorTransformation
from rei.cognitive.channels.cognitive_icons import TensorCognitiveIcon
from rei.cognitive.channels.channel_base_definitions import CognitiveChannel, CognitiveArbiter
from rei.cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge
from rei.cognitive.format.hypergraph.laplacian.graph_metrics import entropy_normalized_laplacian
from rei.cognitive.format.hypergraph.operations.generative_operators import create_dir_edge


def create_tree(taxon_name="test", tree_name="tree", nodes: list[str]|None = None):
    taxon = NetworkTaxonomy(taxon_name, 0)
    test_system = HypergraphNode(tree_name, 0, domain=taxon)
    # Create nodes
    if nodes is not None:
        node_names = [x for x in nodes]
        for n0 in node_names:
            v0 = HypergraphNode(n0, 0)
            test_system.add_subset(v0, 0)
    # Create edges
    return taxon, test_system


def test_tree_basic_3nodes():
    """
    Test the creation of the Fano-graph
    :return:
    """
    _, graph = create_tree(nodes=['A', 'B', 'C'])
    tree_pr = "test/tree/"
    create_dir_edge(graph, tree_pr, ["A"], ["B"])
    create_dir_edge(graph, tree_pr, ["A"], ["C"])
    assert len(graph._subsets) == 5
    print()
    # Print graph
    for set in graph._subsets.values():
        if isinstance(set, HypergraphEdge):
            set.print_elements()
    sys = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, sys.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    ch.encode([graph])
    fragment = view_icon.view()[0]
    # Check elements
    assert fragment.V[0, 1, 0] == 0
    assert fragment.V[0, 0, 1] == 0
    assert fragment.V[1, 2, 0] == 0
    assert fragment.V[1, 0, 1] == 0
    assert fragment.V[1, 0, 0] == 1
    assert fragment.V[2, 0, 1] == 1
    # Check entropy
    eig_val_tensor = entropy_normalized_laplacian(fragment)
    assert eig_val_tensor == 2.0



