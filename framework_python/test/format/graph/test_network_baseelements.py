from rei.foundations.clock import DummyClock
from rei.foundations.identification.identity_generator import Sha3UniqueIdentifierGenerator
from rei.hypergraph.base_elements import HypergraphNode


def test_network_node_qualified_name():
    unique_identifier = Sha3UniqueIdentifierGenerator("test", lambda x, y: f"{x}")
    __clock = DummyClock()
    n0 = HypergraphNode("node0", unique_identifier.generate_uid("test"), "node0", __clock)
    assert n0.qualified_name == "node0"


def test_network_node_register_qualified_name():
    unique_identifier = Sha3UniqueIdentifierGenerator("test", lambda x, y: f"{x}")
    __clock = DummyClock()
    n0 = HypergraphNode("node0", unique_identifier.generate_uid("test"), "node0", __clock)
    taxon = HypergraphNode("taxon", unique_identifier.generate_uid("test"), "taxon", __clock)
    taxon.add_element(n0)

    # Regression test of parents
    assert n0.parent is not None
    assert taxon.parent is None
    assert n0.qualified_name == "taxon/node0"


def test_network_node_reregister_qualified_name():
    unique_identifier = Sha3UniqueIdentifierGenerator("test", lambda x, y: f"{x}")
    __clock = DummyClock()
    n0 = HypergraphNode("node0", unique_identifier.generate_uid("test"), "node0", __clock)
    taxon = HypergraphNode("taxon", unique_identifier.generate_uid("test"), "node0", __clock)
    taxon.add_element(n0)
    taxon2 = HypergraphNode("taxon2", unique_identifier.generate_uid("test"), "node0", __clock)
    taxon2.add_element(n0)

    # Regression test on parents
    assert n0.parent is not None
    assert n0.parent is taxon2
    assert taxon.parent is None
    assert taxon2.parent is None
    assert n0.qualified_name == "taxon2/node0"
