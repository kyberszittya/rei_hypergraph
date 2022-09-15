from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock


class SimpleTestFactory(object):

    @staticmethod
    def create_test_factory():
        __clock = DummyClock()
        __factory = HypergraphFactory("simple_test", __clock)
        return __clock, __factory

    @staticmethod
    def simple_node_without_taxon():
        __clock, __factory = SimpleTestFactory.create_test_factory()
        return __factory.generate_node("node1")

    @staticmethod
    def simple_node_with_default_taxon():
        __clock, __factory = SimpleTestFactory.create_test_factory()
        taxon = __factory.generate_node("network_node")
        n0 = __factory.generate_node("node1", taxon)
        return taxon, n0

    @staticmethod
    def create_nodes_with_default_taxon(arg: list[str]):
        __clock, __factory = SimpleTestFactory.create_test_factory()
        taxon = __factory.generate_node("network_node")
        nodes = []
        for a in arg:
            nodes.append(__factory.generate_node(a, taxon))
        return taxon, nodes


    @staticmethod
    def create_4_nodes():
        __clock, __factory = SimpleTestFactory.create_test_factory()
        taxon = __factory.generate_node("network_node")
        test_system = __factory.generate_node("sys", taxon)
        node_names = {"node1", "node2", "node3", "node4"}
        for n0 in node_names:
            __factory.generate_node(n0, test_system)
        return taxon, test_system
