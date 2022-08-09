from rei.foundations.abstract_items import IdentifiableItem
from rei.foundations.clock import MetaClock
from rei.foundations.conceptual_item import ConceptualItem, HierarchicalElement
from rei.foundations.identification.identity_generator import Sha3UniqueIdentifierGenerator
from rei.hypergraph.common_definitions import EnumRelationDirection

import numpy as np

class HypergraphElement(ConceptualItem):
    """

    """

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None):
        super().__init__(id_name, uuid, qualified_name, clock, parent)
        self._id_generation = Sha3UniqueIdentifierGenerator(id_name,
                                                            HypergraphElement.identification_generation)

    @staticmethod
    def identification_generation(self, x: str, y: IdentifiableItem):
        return f"{x}/{y.id_name}"


class HypergraphRelation(HierarchicalElement):
    """

    """

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str,
                 endpoint: HypergraphElement, parent=None,
                 direction: EnumRelationDirection = EnumRelationDirection.BIDIRECTIONAL):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent)
        self._endpoint = endpoint
        self._direction = direction
        match self._direction:
            case EnumRelationDirection.BIDIRECTIONAL:
                self._relation_incidence_value = np.array([1.0, 1.0])
            case EnumRelationDirection.INWARDS:
                self._relation_incidence_value = np.array([1.0, 0.0])
            case EnumRelationDirection.OUTWARDS:
                self._relation_incidence_value = np.array([0.0, 1.0])

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def direction(self):
        return self._direction

    @property
    def relation_incidence_value(self):
        return np.copy(self._relation_incidence_value)


class HypergraphEdge(HypergraphElement):
    """

    """

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None):
        super().__init__(id_name, uuid, qualified_name, clock, parent)

    def unary_connect(self, endpoint: HypergraphElement,
                      direction: EnumRelationDirection = EnumRelationDirection.BIDIRECTIONAL):
        id_name = "rel"+'.'.join([self.id_name, endpoint.id_name, str(self.clock.get_time_ns())])
        rel = HypergraphRelation(self._id_generation.generate_uid(endpoint.id_name), id_name,
                                 '/'.join([self.id_name, id_name]), endpoint, self, direction)


class HypergraphNode(HypergraphElement):
    """

    """

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,

                 parent: HierarchicalElement = None) -> None:
        super().__init__(id_name, uuid, qualified_name, clock, parent)

    @property
    def sub_edges(self):
        return filter(lambda x: isinstance(x, HypergraphEdge), self._sub_elements.values())

    @property
    def sub_nodes(self):
        return filter(lambda x: isinstance(x, HypergraphNode), self._sub_elements.values())

