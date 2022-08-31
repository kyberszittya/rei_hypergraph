
import pytest

from rei.foundations.common_errors import ErrorRecursiveHierarchy, ErrorDuplicateElement
from test.hypergraph.common_test_hypergraph_functions import dummy_node_test_factory_creation

__QUERY_INTEGRITY_NODE1 = "integrity/node1"


def test_network_taxonomy():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("integrity")
    n1 = __factory.generate_node("node")
    n1.register(taxon)
    assert n1.qualified_name == "integrity/node"


def test_network_taxonomy_multiple_items_qualified_name():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("integrity")
    n1 = __factory.generate_node("node1")
    taxon.add_element(n1)
    assert n1.qualified_name == __QUERY_INTEGRITY_NODE1
    n2 = __factory.generate_node("node2")
    taxon.add_element(n2)
    assert n2.qualified_name == "integrity/node2"


def test_network_taxonomy_multiple_items_uid():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("integrity")
    n1 = __factory.generate_node("node1")
    taxon.add_element(n1)
    assert n1.cid == 0
    n2 = __factory.generate_node("node2")
    taxon.add_element(n2)
    assert n2.cid == 1


def test_network_taxonomy_deregister():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("integrity")
    n1 = __factory.generate_node("node1")
    taxon.add_element(n1)
    n1.deregister()
    assert n1.qualified_name == "node1"


def test_network_reregister_to_same():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("integrity")
    n1 = __factory.generate_node("node1")
    n1.register(taxon)
    n1.deregister()
    n1.register(taxon)
    assert n1.qualified_name == __QUERY_INTEGRITY_NODE1


def test_network_element_update():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("integrity")
    n1 = __factory.generate_node("node1")
    n1.register(taxon)
    n1.update()
    assert n1.qualified_name == __QUERY_INTEGRITY_NODE1


def test_network_reregister_distinct():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon1 = __factory.generate_node("taxa1")
    taxon2 = __factory.generate_node("taxa2")
    n1 = __factory.generate_node("node1")
    n1.register(taxon1)
    taxon2.add_element(n1)
    assert n1.qualified_name == "taxa2/node1"
    assert taxon1.cnt_subelements == 0
    assert taxon2.cnt_subelements == 1


def test_network_register_register_twice():
    __clock, __factory = dummy_node_test_factory_creation()
    taxon1 = __factory.generate_node("taxa1")
    n1 = __factory.generate_node("node1")
    n1.register(taxon1)
    with pytest.raises(ErrorDuplicateElement):
        n1.register(taxon1)
    assert taxon1.cnt_subelements == 1
    assert n1.parent is taxon1


def test_hierarchy_taxonomy_registration():
    _, __factory = dummy_node_test_factory_creation()
    taxon = __factory.generate_node("integrity")
    taxon_sys = __factory.generate_node("sys")
    taxon.register(taxon_sys)
    assert taxon.qualified_name == "sys/integrity"


def test_element_register_loop():
    _, __factory = dummy_node_test_factory_creation()
    with pytest.raises(ErrorRecursiveHierarchy):
        taxon = __factory.generate_node("sys")
        taxon.add_element(taxon)