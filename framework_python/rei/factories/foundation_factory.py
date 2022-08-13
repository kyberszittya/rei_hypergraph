import typing

from rei.foundations.clock import MetaClock
from rei.foundations.identification.identity_generator import Sha3UniqueIdentifierGenerator
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge
from rei.hypergraph.value_node import ValueNode


class HypergraphFactory():

    def __init__(self, factory_name: str, clock: MetaClock) -> None:
        super().__init__()
        self._factory_name: str = factory_name
        self._clock: MetaClock = clock
        self.unique_identifier = Sha3UniqueIdentifierGenerator(
            self._factory_name, lambda x, y: f"{x}/{self.get_qualified_name(y)}")

    def get_qualified_name(self, name: str):
        return f"{name}.{self._clock.get_time_ns()}"

    def generate_node(self, id_name: str, parent: HypergraphNode = None) -> HypergraphNode:
        node = HypergraphNode(id_name, self.unique_identifier.generate_uid(id_name),
                              '/'.join([self._factory_name, self.get_qualified_name(id_name)]),
                              self._clock, parent)
        return node

    #
    # Generator functions
    #

    def create_hyperedge(self, parent: HypergraphNode, edge_name: str):
        uuid: bytes = self.unique_identifier.generate_uid(edge_name)
        he = HypergraphEdge(edge_name, uuid,
                            '/'.join([parent.qualifed_name, edge_name])+f".{parent.clock.get_time_ns()}",
                            parent.clock, parent)
        return he

    def create_value(self, parent: HypergraphNode | None, value_name: str, values: list[typing.Any] = None):
        uuid: bytes = self.unique_identifier.generate_uid(value_name)
        if parent is not None:
            val = ValueNode(uuid, value_name,
                            '/'.join([parent.qualifed_name, value_name])+f".{parent.clock.get_time_ns()}",
                            values)
            parent.add_element(val)
        else:
            val = ValueNode(uuid, value_name,
                            '/'.join([value_name])+f".{self._clock.get_time_ns()}",
                            values)
        return val

