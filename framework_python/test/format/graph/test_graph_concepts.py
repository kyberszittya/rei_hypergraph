from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode
from cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy

from test.format.common_test_factories import SimpleTestFactory, default_identifier_generator


def test_basic_identification_no_domain():
    """
    Test basic identification generation with SHA3-224 ID
    :return:
    """
    n_0 = SimpleTestFactory.simple_node_without_taxon()
    assert(n_0.uid.hex() == '6088fc5a1333dcf81dfc56e7add8f85cd4837f4893623083c037b8f8')


def test_basic_identification_0():
    """
    Test basic identification generation with SHA3-224 ID
    :return:
    """
    _, n_0 = SimpleTestFactory.simple_node_with_default_taxon()
    assert(n_0.uid.hex() == '526561067a58ad223d7db61c952f0e43c43df1227cc0b683b0d35985')


def test_2_node_identification():
    """
    Test whether 2 nodes have distinct identifiers
    :return:
    """
    _, nodes = SimpleTestFactory.create_nodes_with_default_taxon(["node1", "node2"])
    assert(nodes[0].uid.hex() == '526561067a58ad223d7db61c952f0e43c43df1227cc0b683b0d35985')
    assert(nodes[1].uid.hex() != '526561067a58ad223d7db61c952f0e43c43df1227cc0b683b0d35985')


def test_basic_identity_id_varying_timestamp():
    """
    Test the identification with simple texts
    :return:
    """
    registrar = default_identifier_generator()
    id_item = registrar.generate_id("item1", 0)
    assert id_item.hex() == "ed7af8c6eef44a70b31111057acecb4642ffd769f42629f1076cfdf3"
    id_item = registrar.generate_id("item1", 1000)
    assert id_item.hex() != "ed7af8c6eef44a70b31111057acecb4642ffd769f42629f1076cfdf3"
    assert id_item.hex() == "bffa3380a53170c9db8cd80a5a8180056dbaa829c71615fcab4bfa49"


def test_create_hierarchy():
    """
    Test simple hierarchy of hypergraph nodes
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2"}
    for n in node_names:
        n0 = HypergraphNode(n, 0)
        test_system.add_subset(n0, 0)
        assert n0.parent is test_system
    assert len(test_system._subsets.values()) == 2
    for v in test_system._subsets.values():
        assert isinstance(v, HypergraphNode)
        assert v.progenitor_registry.name in node_names
    print()
    test_system.print_hierarchy_tree()
    assert len(taxon.registered_items.values()) == 1


def test_create_hierarchy_operator():
    """
    Test simple hierarchy of hypergraph nodes
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2"}
    for n in node_names:
        n0 = HypergraphNode(n, 0)
        test_system += n0
        assert n0.parent is test_system
    assert len(test_system._subsets.values()) == 2
    for v in test_system._subsets.values():
        assert isinstance(v, HypergraphNode)
        assert v.progenitor_registry.name in node_names
    print()
    test_system.print_hierarchy_tree()
    assert len(taxon.registered_items.values()) == 1


def test_create_hierarchy2():
    """
    Test simple hierarchy of hypergraphnodes
    :return:
    """
    taxon = NetworkTaxonomy("network_node", 0)
    test_system = HypergraphNode("sys", 0, domain=taxon)
    node_names = {"node1", "node2"}
    for n0 in node_names:
        v0 = HypergraphNode(n0, 0)
        test_system.add_subset(v0, 0)
        assert v0.parent is test_system
        for n1 in node_names:
            v1 = HypergraphNode(n1, 0)
            v0.add_subset(v1, 0)
            assert v1.parent is v0
    assert len(test_system._subsets.values()) == 2
    for v in test_system._subsets.values():
        assert isinstance(v, HypergraphNode)
        assert v.progenitor_registry.name in node_names
    for v in test_system._subsets.values():
        for v0 in v._subsets.values():
            assert v0.uid != v.uid
            assert v0.id_name in node_names
    print()
    test_system.print_hierarchy_tree()
    assert len(taxon.registered_items.values()) == 1

