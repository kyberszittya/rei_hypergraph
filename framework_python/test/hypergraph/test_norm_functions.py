from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock

from rei.hypergraph.norm_functions import sum_norm
from rei.hypergraph.value_node import ValueNode


def test_sum_norm():
    __clock = DummyClock()
    __factory = HypergraphFactory("fac",  __clock)
    v: ValueNode = __factory.create_value(None, "val0", [1.0])
    assert sum_norm(v.val) == 1.0


def test_sum_norm_2():
    __clock = DummyClock()
    __factory = HypergraphFactory("fac",  __clock)
    v: ValueNode = __factory.create_value(None, "val0", [1.0, 4.0, -2.0])
    assert sum_norm(v.val) == 3.0
