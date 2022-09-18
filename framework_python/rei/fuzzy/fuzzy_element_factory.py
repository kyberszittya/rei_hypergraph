from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import MetaClock
from rei.fuzzy.fuzzy_engine import FuzzyEngine
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.value_node import SemanticValueNode


class FuzzyElementFactory(HypergraphFactory):

    def __init__(self, factory_name: str, clock: MetaClock) -> None:
        super().__init__(factory_name, clock)

    def create_fuzzy_engine(self, id_name: str, parent: HypergraphNode = None) -> FuzzyEngine:
        if parent is not None:
            uid = self.unique_identifier.generate_uid('/'.join([parent.qualified_name, id_name]))
        else:
            uid = self.unique_identifier.generate_uid(id_name)
        node = FuzzyEngine(id_name, uid, '/'.join([self._factory_name, self.get_qualified_name(id_name)]),
                           self._clock, parent)
        return node

    def create_fuzzy_computation_node(self, id_name: str,
                                      values: list,
                                      parent: HypergraphNode = None):
        __node = self.generate_node(id_name, parent)
        __values = self.create_value(__node, "values", values)
        return __node, __values

    def connect_fuzzy_nodes(
            self, id_name: str, parent: HypergraphNode, tnorm, snorm,
            connections: list[tuple[HypergraphNode, EnumRelationDirection, dict | list, SemanticValueNode | None]]):
        __fhe: HypergraphEdge = self.connect_tuple_nodes(parent, id_name, connections)
        self.create_value(__fhe, "snorm", [snorm])
        self.create_value(__fhe, "tnorm", [tnorm])
        return __fhe
