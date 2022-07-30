
from rei.cognitive.format.hypergraph.special_graphs import fano_graph
from rei.cognitive.format.hypergraph.laplacian.graph_tensor_operations import laplacian_calc_vector, \
    graph_upper_bound_entropy_vector, graph_bound_entropy, laplacian_calc_tensor

import time

def test_fano_laplacian_calculation():
    A = fano_graph()
    total_deg = 0
    # Naive calculation of Laplacian
    start_time = time.perf_counter_ns()
    D, L, total_deg = laplacian_calc_tensor(A)
    end_time = time.perf_counter_ns()
    # Vectorized calculation of Laplacian
    start_time_v = time.perf_counter_ns()
    _, laplace_v, deg_v = laplacian_calc_vector(A)
    end_time_v = time.perf_counter_ns()
    print(laplace_v, L)
    print(f"Time NS, naive {end_time - start_time}, vector: {end_time_v - start_time_v}")
    # TODO: REVISE
    # assert total_deg == deg_v


def test_laplacian_1():
    A = fano_graph()
    start_time = time.perf_counter_ns()
    entropy = graph_bound_entropy(A)
    end_time = time.perf_counter_ns()
    start_time_v = time.perf_counter_ns()
    entropy_v = graph_upper_bound_entropy_vector(A)[0]
    end_time_v = time.perf_counter_ns()
    assert entropy != entropy_v
    print(f"Time NS, naive {end_time - start_time}, vector: {end_time_v - start_time_v}")

