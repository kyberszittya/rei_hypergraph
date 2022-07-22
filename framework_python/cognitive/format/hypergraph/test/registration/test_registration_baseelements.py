from cognitive.format.basicelements.concepts.network.taxonomy import \
    NetworkTaxonomy, NetworkRegistryItem, ErrorRegistry

import pytest

def test_network_taxonomy():
    taxon = NetworkTaxonomy("integrity", 0)
    n1 = NetworkRegistryItem("node", 0)
    n1.register(taxon, 0)
    assert n1.qualified_name == "integrity/node"


def test_network_taxonomy_multiple_items_qualified_name():
    taxon = NetworkTaxonomy("integrity", 0)
    n1 = NetworkRegistryItem("node1", 0)
    n1.register(taxon, 0)
    assert n1.qualified_name == "integrity/node1"
    n2 = NetworkRegistryItem("node2", 0)
    n2.register(taxon, 0)
    assert n2.qualified_name == "integrity/node2"


def test_network_taxonomy_multiple_items_uid():
    taxon = NetworkTaxonomy("integrity", 0)
    n1 = NetworkRegistryItem("node1", 0)
    n1.register(taxon, 0)
    assert n1.uuid == b'\x00\x00\x00\x00\x00\x00\x00'
    n2 = NetworkRegistryItem("node2", 0)
    n2.register(taxon, 0)
    assert n2.uuid == b'\x00\x00\x00\x00\x00\x00\x01'


def test_network_taxonomy_deregister():
    taxon = NetworkTaxonomy("integrity", 0)
    n1 = NetworkRegistryItem("node1", 0)
    n1.register(taxon, 0)
    n1.deregister()


def test_network_reregister_to_same():
    taxon = NetworkTaxonomy("integrity", 0)
    n1 = NetworkRegistryItem("node1", 0)
    n1.register(taxon, 0)
    n1.deregister()
    n1.register(taxon, 0)
    assert n1.qualified_name == "integrity/node1"


def test_network_reregister_to_same2():
    taxon = NetworkTaxonomy("integrity", 0)
    n1 = NetworkRegistryItem("node1", 0)
    n1.register(taxon, 0)
    n1.reregister(taxon, 0)
    assert n1.qualified_name == "integrity/node1"


def test_network_reregister_distinct():
    taxon1 = NetworkTaxonomy("taxa1", 0)
    taxon2 = NetworkTaxonomy("taxa2", 0)
    n1 = NetworkRegistryItem("node1", 0)
    n1.register(taxon1, 0)
    n1.reregister(taxon2, 0)
    assert n1.qualified_name == "taxa2/node1"
    assert len(taxon1.registered_items.values()) == 0
    assert len(taxon2.registered_items.values()) == 1


def test_network_register_register_twice():
    with pytest.raises(ErrorRegistry):
        taxon1 = NetworkTaxonomy("taxa1", 0)
        n1 = NetworkRegistryItem("node1", 0)
        n1.register(taxon1, 0)
        n1.register(taxon1, 0)


def test_hierarchy_taxonomy_registration():
    taxon = NetworkTaxonomy("integrity", 0)
    taxon_sys = NetworkTaxonomy("sys", 0)
    taxon.register(taxon_sys, 0)
    assert taxon.qualified_name == "sys/integrity"


def test_element_register_loop():
    with pytest.raises(ErrorRegistry):
        taxon = NetworkTaxonomy("sys", 0)
        taxon.register(taxon, 0)