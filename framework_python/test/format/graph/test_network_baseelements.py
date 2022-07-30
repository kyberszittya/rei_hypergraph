from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkNode
from rei.cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import \
    IdentifierGeneratorSha224


def test_network_node_qualified_name():
    n0 = NetworkNode("node0", 0, IdentifierGeneratorSha224(""), None)
    assert n0.progenitor_registry.qualified_name == "node0"


def test_network_node_register_qualified_name():
    n0 = NetworkNode("node0", 0, IdentifierGeneratorSha224(""), None)
    taxon = NetworkTaxonomy("taxon", 0)
    n0.register(taxon, 0)

    # Regression test of parents
    assert n0.progenitor_registry._parent_registry is not None
    assert n0.progenitor_registry._parent_registry is taxon
    assert taxon._parent_registry is None
    assert n0.progenitor_registry.qualified_name == "taxon/node0"


def test_network_node_reregister_qualified_name():
    n0 = NetworkNode("node0", 0, IdentifierGeneratorSha224(""), None)
    taxon = NetworkTaxonomy("taxon", 0)
    n0.register(taxon, 0)
    taxon2 = NetworkTaxonomy("taxon2", 0)
    n0.register(taxon2, 0)

    # Regression test on parents
    assert n0.progenitor_registry._parent_registry is not None
    assert n0.progenitor_registry._parent_registry is taxon2
    assert taxon._parent_registry is None
    assert taxon2._parent_registry is None
    assert n0.progenitor_registry.qualified_name == "taxon2/node0"
