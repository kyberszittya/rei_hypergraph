from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode
from cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy

from test.format.common_test_factories import SimpleTestFactory


def test_basic_identification_no_domain():
    """
    Test basic identification generation with SHA3-224 ID
    :return:
    """
    n0 = SimpleTestFactory.simple_node_without_taxon()
    assert n0.progenitor_registry.uuid is None
    assert n0.progenitor_registry.qualified_name == "node1"


def test_basic_registry_0():
    """
    Basic registration of node

    """
    _, n0 = SimpleTestFactory.simple_node_with_default_taxon()
    assert(int.from_bytes(n0.progenitor_registry.uuid, byteorder='big') == 0)
    assert n0.progenitor_registry.qualified_name == "network_node/node1"

def test_qualified_name_single_node():
    """
    Test qualified names
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    assert test_system.progenitor_registry.qualified_name == "network_node/sys"


def test_duplicate_register():
    taxon = NetworkTaxonomy("network_node", 0)
    n0 = HypergraphNode("n0", 0)
    n0.register(taxon, 0)



def test_change_taxon():
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    taxon_new = NetworkTaxonomy("network2", 0)
    test_system.register(taxon_new, 0)


def test_qualified_name_hierarchy():
    """
    Test qualified names in a hierarchy
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2", "node3", "node4"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
    qualified_names = set(['network_node/sys/'+v for v in node_names])
    for v in test_system._subsets.values():
        assert v.progenitor_registry.qualified_name in qualified_names
    assert len(taxon.registered_items.values()) == 1


def test_qualified_name_hierarchy_no_taxon():
    """
    Test qualified names in a hierarchy
    :return:
    """
    test_system = HypergraphNode("sys", 0)
    node_names = {"node1", "node2", "node3", "node4"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
    qualified_names = set(['sys/'+v for v in node_names])
    for v in test_system._subsets.values():
        assert v.progenitor_registry.qualified_name in qualified_names


def test_qualified_name_hierarchy_change_taxon():
    """
    Test qualified names in a hierarchy
    :return:
    """
    test_system = HypergraphNode("sys", 0)
    node_names = {"node1", "node2", "node3", "node4"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
    taxon = NetworkTaxonomy("taxon", 0)
    test_system.register(taxon, 0)
    qualified_names = set(['taxon/sys/'+v for v in node_names])
    for v in test_system._subsets.values():
        assert v.progenitor_registry.qualified_name in qualified_names
