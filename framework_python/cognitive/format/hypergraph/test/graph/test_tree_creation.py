from cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from cognitive.format.hypergraph.channels.tensor_channel import CognitiveChannel, TensorCognitiveIcon, \
    HypergraphTensorTransformation, CognitiveArbiter
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge
from cognitive.format.hypergraph.foundations.hypergraph_operators import create_dir_edge
from cognitive.format.hypergraph.laplacian.graph_tensor_operations import graph_upper_bound_entropy_vector, \
    laplacian_calc_vector


def create_tree(taxon_name="test", tree_name="tree", nodes: list[str]=[]):
    taxon = NetworkTaxonomy(taxon_name, 0)
    test_system = HypergraphNode(tree_name, 0, domain=taxon)
    # Create nodes
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
    _, graph = create_tree(nodes=['A','B','C'])
    tree_pr = "test/tree/"
    create_dir_edge(graph, tree_pr, ["A"], ["B"])
    create_dir_edge(graph, tree_pr, ["A"], ["C"])
    assert len(graph._subsets) == 5
    # Print graph
    for set in graph._subsets.values():
        if isinstance(set, HypergraphEdge):
            set.print_elements()
    sys = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, sys.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    tensor = ch.encode([graph])
    # Check elements
    assert tensor[0,1,0] == -1
    assert tensor[0,0,1] == 1
    assert tensor[1,2,0] == -1
    assert tensor[1,0,2] == 1
    # Check entropy
    eig_val_tensor = graph_upper_bound_entropy_vector(tensor)
    assert eig_val_tensor == 1.0
    # Check whether Laplacian equals to tree adjacency matrix
    import numpy as np
    L_tensor = np.sum(laplacian_calc_vector(tensor)[1], axis=0)
    A = np.array([[0, 1, 1],
                  [-1, 0, 0],
                  [-1, 0, 0]])
    D = np.diag([2,1,1])
    L = D - A
    assert np.array_equal(L, L_tensor)
    assert np.trace(L)/4 == eig_val_tensor
    # Pure laplacian calculation
    L_struct = np.array([[ 2, -1, -1],
                         [-1,  1,  0],
                         [-1,  0,  1]])
    _eig = np.linalg.eig(L_struct)[0]/4
    entropy_analytic = -np.sum(np.nan_to_num(_eig*np.log2(_eig)))
    assert entropy_analytic <= eig_val_tensor
    print(f"Analytical entropy: {entropy_analytic}")
    print()