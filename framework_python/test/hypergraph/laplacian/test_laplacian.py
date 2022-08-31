import asyncio
import time

from rei.foundations.clock import DummyClock
from rei.hypergraph.sample_graphs.fano_graph import create_fano_graph
from rei.tensor.tensor_representation import NumpyHypergraphTensorTransformer


def test_fano_laplacian_calculation():
    _, __n0, __node_list, __edges = create_fano_graph("fano_test", DummyClock())
    tr = NumpyHypergraphTensorTransformer()
    asyncio.run(tr.execute(__n0))
    # Naive calculation of Laplacian
    start_time = time.perf_counter_ns()
    entropy = tr.tensor_representation.entropy()
    end_time = time.perf_counter_ns()
    # Vectorized calculation of Laplacian
    start_time_v = time.perf_counter_ns()
    laplace = tr.tensor_representation.entropy_vector()
    end_time_v = time.perf_counter_ns()
    print(entropy, laplace)
    print(f"Time NS, naive {end_time - start_time}, vector: {end_time_v - start_time_v}")



def test_laplacian_1():
    _, __n0, __node_list, __edges = create_fano_graph("fano_test", DummyClock())
    tr = NumpyHypergraphTensorTransformer()
    asyncio.run(tr.execute(__n0))
    start_time = time.perf_counter_ns()
    tr.tensor_representation.entropy()
    end_time = time.perf_counter_ns()
    start_time_v = time.perf_counter_ns()
    tr.tensor_representation.entropy_vector()
    end_time_v = time.perf_counter_ns()
    print(f"Time NS, naive {end_time - start_time}, vector: {end_time_v - start_time_v}")

