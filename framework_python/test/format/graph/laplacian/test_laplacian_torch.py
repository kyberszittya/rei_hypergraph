from cognitive.format.hypergraph.torch.special_graphs import fano_graph

def test_fano_graph_laplacian():
    A = fano_graph()
    print(A)