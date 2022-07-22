
import numpy as np

import time

from special_graphs import fano_graph
from cognitive.format.hypergraph.laplacian.graph_tensor_operations import graph_bound_entropy

def fano_graph_example():
    adj_fano = fano_graph()
    naive_start_time = time.perf_counter_ns()

    proj_adj = np.sum(adj_fano, axis=0)
    #
    d = np.sum(proj_adj, axis=0)
    naive_laplacian = np.diag(d) - proj_adj

    eig_naive_v, eig_naive_w = np.linalg.eig(naive_laplacian)

    norm_eig_naive_v = eig_naive_v / np.sum(d)

    naive_entropy = -np.sum(norm_eig_naive_v * np.log2(np.abs(norm_eig_naive_v)))
    naive_end_time = time.perf_counter_ns()
    print(naive_end_time - naive_start_time)
    print(naive_laplacian)
    print(eig_naive_v)
    print(f"Normalized eigenvalues: {norm_eig_naive_v}")
    print(f"Naive entropy: {naive_entropy}")
    #
    new_start_time = time.perf_counter_ns()
    total_entropy = graph_bound_entropy(adj_fano)
    new_end_time = time.perf_counter_ns()
    print(new_end_time - new_start_time)
    print(f"Upper bound entropy: {total_entropy}")
    total_entropy_lower = graph_bound_entropy(np.swapaxes(adj_fano,0,1))
    print(f"Lower bound entropy: {total_entropy_lower}")
    print((total_entropy_lower+total_entropy)/2.0)


def main():
    fano_graph_example()


if __name__ == "__main__":
    main()