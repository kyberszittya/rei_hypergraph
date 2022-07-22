from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode
from cognitive.format.basicelements.concepts.registry.registration_methods import IdentifierGeneratorSha224
from cognitive.format.basicelements.concepts.network.taxonomy import NetworkTaxonomy


def default_identifier_generator():
    return IdentifierGeneratorSha224("simple_identity")


class SimpleTestFactory(object):

    @staticmethod
    def simple_node_without_taxon():
        return HypergraphNode("node1", 0)

    @staticmethod
    def simple_node_with_default_taxon():
        taxon = NetworkTaxonomy("network_node", 0)
        n0 = HypergraphNode("node1", 0, domain=taxon)
        return taxon, n0

    @staticmethod
    def create_nodes_with_default_taxon(arg: list[str]):
        taxon = NetworkTaxonomy("network_node", 0)
        nodes = []
        for a in arg:
            nodes.append(HypergraphNode(a, 0, domain=taxon))
        return taxon, nodes


    @staticmethod
    def create_4_nodes():
        taxon = NetworkTaxonomy("network_node", 0)
        test_system = HypergraphNode("sys", 0, domain=taxon)
        node_names = {"node1", "node2", "node3", "node4"}
        for n0 in node_names:
            v0 = HypergraphNode(n0, 0)
            test_system.add_subset(v0, 0)
        return taxon, test_system
