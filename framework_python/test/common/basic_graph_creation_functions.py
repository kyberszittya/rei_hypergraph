from rei.cognitive.channels.channel_base_definitions import CognitiveArbiter, CognitiveChannel
from rei.cognitive.channels.cognitive_dendrite import HypergraphTensorTransformation
from rei.cognitive.channels.cognitive_icons import TensorCognitiveIcon
from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from rei.cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode
from rei.cognitive.format.hypergraph.operations.generative_operators import create_hyperedge, create_dir_edge

#
# Segment: FANO GRAPH
#
from rei.cognitive.messages.tensor_fragment import FragmentTensor


def create_fano_edge(sys: HypergraphNode, qualified_name: str, nodes: list[str]):
    sys.add_subset(
        create_hyperedge("e"+''.join(nodes), 0, sys,
                         [(qualified_name+x, EnumRelationDirection.UNDIRECTED) for x in nodes]), 0)


def create_fano_graph():
    taxon = NetworkTaxonomy("test", 0)
    test_system = HypergraphNode("fano_graph", 0, domain=taxon)
    # Create nodes
    node_names = ["0", "1", "2", "3", "4", "5", "6"]
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


def setup_test_graph_elements(taxon, graph) -> FragmentTensor:
    sys = CognitiveArbiter(name="sys", timestamp=0, domain=taxon)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0, domain=taxon)
    ch = HypergraphTensorTransformation("dendrite1", 0, taxon, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    ch.encode([graph])
    fragment = view_icon.view()[0]
    return fragment

#
# END SEGMENT: FANO GRAPH
#


#
# Segment: Multi-tree
#


def create_multitree():
    taxon = NetworkTaxonomy("test", 0)
    test_system = HypergraphNode("multitree", 0, domain=taxon)
    # Create nodes
    node_names = ["0", "1", "2", "3", "4", "5", "6"]
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

#
# END SEGMENT: Simple Multi-tree
#

#
# Segment: simple tree
#

def create_simple_tree():
    taxon = NetworkTaxonomy("test", 0)
    test_system = HypergraphNode("simpletree", 0, domain=taxon)
    # Create nodes
    node_names = ["0", "1", "2"]
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
    # Create edges
    tree_pr = "test/simpletree/"
    create_dir_edge(test_system, tree_pr, ["0"], ["1"])
    create_dir_edge(test_system, tree_pr, ["0"], ["2"])
    return taxon, test_system