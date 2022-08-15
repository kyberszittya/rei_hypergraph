import typing

from rei.foundations.abstract_items import IdentifiableItem
from rei.foundations.clock import MetaClock
from rei.foundations.conceptual_item import ConceptualItem, HierarchicalElement
from rei.foundations.identification.identity_generator import Sha3UniqueIdentifierGenerator
from rei.hypergraph.common_definitions import EnumRelationDirection

import numpy as np

from rei.hypergraph.value_node import ValueNode


class HypergraphPort(HierarchicalElement):
    """

    """

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, endpoint: HierarchicalElement,
                 parent=None) -> None:
        super().__init__(uuid, id_name, progenitor_qualified_name, parent)
        self._endpoint = endpoint


class HypergraphElement(ConceptualItem):
    """

    """

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None):
        super().__init__(id_name, uuid, qualified_name, clock, parent)
        self._id_generation = Sha3UniqueIdentifierGenerator(id_name, HypergraphElement.identification_generation)
        # Ports to deduce associated relations
        self._ports: dict[bytes, HypergraphPort] = {}

    @staticmethod
    def identification_generation(x: str, y: IdentifiableItem):
        return f"{x}/{y.id_name}"

    def connect(self, el: HierarchicalElement):
        port_name = '.'.join([self.id_name, "port", el.id_name])
        p = HypergraphPort(self._id_generation.generate_uid(port_name), port_name,
                           port_name, el, self)
        self._ports[el.uuid] = p
        self.add_element(p)

    def disconnect(self, el: HierarchicalElement):
        p = self._ports.pop(el.uuid)
        self.remove_element(id_name=p.id_name, uuid=p.uuid)

    @property
    def sub_ports(self):
        yield from self.get_subelements(lambda x: isinstance(x, HypergraphPort))


class HypergraphRelation(HierarchicalElement):
    """

    """

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str,
                 endpoint: HypergraphElement, weight: ValueNode | None, parent=None,
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
        # Weight
        self._weight = weight

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def direction(self):
        return self._direction

    @property
    def relation_incidence_value(self):
        return np.copy(self._relation_incidence_value)

    @property
    def weight(self) -> ValueNode:
        return self._weight

    def update(self):
        self._qualified_name = '/'.join(list(self.update_qualified_name())[::-1])

    def add_element(self, element: HypergraphElement) -> None:
        self._endpoint = element
        self._sub_elements[element.uuid] = element
        # Set port
        element.connect(self)

    def remove_element(self, id_name: str = "", uuid: bytes = None) -> typing.Generator:
        el = self._sub_elements.pop(self.endpoint.uuid)
        self._endpoint = None
        yield el


class HypergraphEdge(HypergraphElement):
    """

    """

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None):
        super().__init__(id_name, uuid, qualified_name, clock, parent)
        self._sub_relations = {}

    def unary_connect(self, endpoint: HypergraphElement, weight: ValueNode,
                      direction: EnumRelationDirection = EnumRelationDirection.BIDIRECTIONAL):
        id_name = "rel"+'.'.join([self.id_name, endpoint.id_name, str(self.clock.get_time_ns())])
        rel = HypergraphRelation(self._id_generation.generate_uid(endpoint), id_name,
                                 '/'.join([self.id_name, id_name]), endpoint, weight, direction=direction)
        self.add_element(rel)

    def add_element(self, element: HierarchicalElement):
        super().add_element(element)
        match element:
            case HypergraphRelation():
                self._sub_relations[element.cid] = element

    def remove_element(self, id_name: str = "", uuid: bytes = None) -> typing.Generator:
        _el = super().remove_element(id_name, uuid)
        for v in _el:
            yield from self._sub_relations.pop(v.cid)

    @property
    def sub_relations(self):
        yield from self.get_subelements(lambda x: isinstance(x, HypergraphRelation))

    @property
    def induced_subset(self) -> typing.Generator:
        yield from map(lambda x: x.endpoint, self.get_subelements(lambda x: isinstance(x, HypergraphRelation)))


class HypergraphNode(HypergraphElement):
    """

    """

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None) -> None:
        super().__init__(id_name, uuid, qualified_name, clock, parent)

    @property
    def sub_edges(self):
        yield from self.get_subelements(lambda x: isinstance(x, HypergraphEdge))

    @property
    def sub_nodes(self):
        yield from self.get_subelements(lambda x: isinstance(x, HypergraphNode))

    @property
    def sub_values(self):
        yield from self.get_subelements(lambda x: isinstance(x, ValueNode))

    def __getitem__(self, uuid: bytes):
        return self._sub_elements[uuid]
