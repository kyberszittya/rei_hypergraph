import numpy as np

from rei.hypergraph.value_node import ValueNode


def sum_norm(arg: ValueNode):
    return np.sum(np.array(arg))
