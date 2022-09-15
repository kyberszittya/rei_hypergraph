from rei.hypergraph.base_elements import HypergraphNode
from test.format.common_test_factories import SimpleTestFactory
from test.hypergraph.common_test_hypergraph_functions import dummy_node_test_factory_creation


def test_basic_identification_no_domain():
    """
    Test basic identification generation with SHA3-224 ID
    :return:
    """
    n0 = SimpleTestFactory.simple_node_without_taxon()
    assert n0.uuid is not None
    assert n0.qualified_name == "node1"


def test_basic_registry_0():
    """
    Basic registration of node

    """
    _, n0 = SimpleTestFactory.simple_node_with_default_taxon()
    assert(n0.cid == 0)
    assert n0.qualified_name == "network_node/node1"

def test_qualified_name_single_node():
    """
    Test qualified names
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", parent=taxon)
    assert test_system.qualified_name == "network_node/sys"


def test_duplicate_register():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon: HypergraphNode = __factory.generate_node("network_node")
    n0 = __factory.generate_node("n0")
    taxon.add_element(n0)
    assert n0.parent is taxon



def test_change_taxon():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", parent=taxon)
    taxon_new = __factory.generate_node("network2")
    taxon_new.add_element(test_system)
    assert test_system.parent is taxon_new
    assert taxon_new.cnt_subelements == 1
    # Check the element is not part of the old node
    assert taxon.cnt_subelements == 0


def test_qualified_name_hierarchy():
    """
    Test qualified names in a hierarchy
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("network_node")
    test_system = __factory.generate_node("sys", parent=taxon)
    node_names = {"node1", "node2", "node3", "node4"}
    for n0 in node_names:
        __factory.generate_node(n0, parent=test_system)
    qualified_names = set(['network_node/sys/'+v for v in node_names])
    for v in test_system.get_subelements(lambda x: True):
        assert v.qualified_name in qualified_names
    assert taxon.cnt_subelements == 1


def test_qualified_name_hierarchy_no_taxon():
    """
    Test qualified names in a hierarchy
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    test_system = __factory.generate_node("sys")
    node_names = {"node1", "node2", "node3", "node4"}
    for n0 in node_names:
        v0 = __factory.generate_node(n0)
        test_system.add_element(v0)
    qualified_names = set(['sys/'+v for v in node_names])
    for v in test_system.get_subelements(lambda x: True):
        assert v.qualified_name in qualified_names


def test_qualified_name_hierarchy_change_taxon():
    """
    Test qualified names in a hierarchy
    :return:
    """
    __clock, __factory = dummy_node_test_factory_creation()
    test_system = __factory.generate_node("sys")
    node_names = {"node1", "node2", "node3", "node4"}
    for n0 in node_names:
        v0 = __factory.generate_node(n0)
        test_system.add_element(v0)
    taxon = __factory.generate_node("taxon")
    taxon.add_element(test_system)
    qualified_names = set([f'taxon/sys/{v}' for v in node_names])
    for v in test_system.get_subelements(lambda x: True):
        assert v.qualified_name in qualified_names
