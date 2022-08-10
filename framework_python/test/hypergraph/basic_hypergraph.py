from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock

__TEST_HYPERGRAPH_FACTORY = "test.hypergraphnode"
__FIRST_NODE = "node"


def dummy_node_test_creation():
    __clock = DummyClock()
    __factory = HypergraphFactory(__TEST_HYPERGRAPH_FACTORY,  __clock)
    return __clock, __factory


def test_single_hypergraph_node():
    __clock, __factory = dummy_node_test_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    assert n0.progenitor_qualified_name == '/'.join([__TEST_HYPERGRAPH_FACTORY, __FIRST_NODE])+".0"
    assert n0.uuid.hex() == "76cf5955e61190bbacd6e0b28f7ee2d095f083ea3945456952b646b1"
    assert n0.id_name == __FIRST_NODE


def test_3_isolated_nodes():
    __clock, __factory = dummy_node_test_creation()
    n0 = __factory.generate_node(__FIRST_NODE)
    for i in range(2):
        __factory.generate_node(__FIRST_NODE+str(i), n0)
    assert n0.cnt_subelements == 2
