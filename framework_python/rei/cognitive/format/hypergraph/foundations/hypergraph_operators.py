import queue
from enum import IntEnum

from rei.cognitive.format.basicelements.concepts.registry.registration_methods import \
    InterfaceIdentifierGenerator
from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkElement, EnumRelationDirection
from rei.cognitive.format.hypergraph.foundations.graph_operations import MetaHypergraphQuery
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge, \
    HypergraphReferenceConnection


class HypergraphCompartmentQuery(MetaHypergraphQuery):
    """
    Query the components (subsets) of a given hypergraph(node)
    """

    def __init__(self, cursor: NetworkElement, id_name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(cursor, id_name, timestamp, identitygen)
        self._parameters["closed_elements"] = set()

    @staticmethod
    def _lookup_hierarchy(cursor: NetworkElement, lookup_name: str, closed_set: set[NetworkElement]):
        if cursor.progenitor_registry.qualified_name == lookup_name:
            yield cursor
        else:
            for v in cursor._subsets.values():
                if v not in closed_set:
                    yield from HypergraphCompartmentQuery._lookup_hierarchy(v, lookup_name, closed_set)

    def execute(self):
        for c in self._cursor:
            yield from HypergraphCompartmentQuery._lookup_hierarchy(c,
                                                                    self._parameters["lookup_name"],
                                                                    self._parameters["closed_elements"])

    def set_lookup_name(self, lookup_name: str):
        self._parameters["lookup_name"] = lookup_name

    def set_closed_elements(self, arg: set[NetworkElement]):
        self._parameters["closed_elements"] = arg


def retrieve_part_hypergraph_node(context: HypergraphNode, qualified_name: str):
    query = HypergraphCompartmentQuery(context, "lookup_query", 0)
    query.set_lookup_name(qualified_name)
    return query.execute()


class HypergraphBidirectionalCompartmentQuery(HypergraphCompartmentQuery):
    """

    """

    def __init__(self, cursor: NetworkElement, id_name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(cursor, id_name, timestamp, identitygen)

    def execute(self):
        closed_set: set = self._parameters["closed_elements"]
        for cursor in self._cursor:
            _current_cursor = cursor
            while _current_cursor is not None:
                yield from HypergraphCompartmentQuery. \
                    _lookup_hierarchy(_current_cursor, self._parameters["lookup_name"],
                                      closed_set)
                closed_set.add(_current_cursor)
                _current_cursor = _current_cursor.parent


class HypergraphDepthBidirectionalCompartmentQuery(HypergraphCompartmentQuery):
    """

    """

    def __init__(self, cursor: NetworkElement, id_name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(cursor, id_name, timestamp, identitygen)

    @staticmethod
    def _depth_lookup_hierarchy(cursor: NetworkElement, lookup_name: str,
                                closed_set: set[NetworkElement],
                                current_depth: int, depth_limit: int):
        if cursor.progenitor_registry.qualified_name == lookup_name and current_depth == depth_limit:
            yield cursor
        else:
            for v in cursor._subsets.values():
                if v not in closed_set:
                    yield from HypergraphDepthBidirectionalCompartmentQuery \
                        ._depth_lookup_hierarchy(v, lookup_name, closed_set, current_depth+1, depth_limit)

    def execute(self):
        current_depth = 0
        closed_set: set = self._parameters["closed_elements"]
        for cursor in self._cursor:
            _current_cursor = cursor
            while _current_cursor is not None:
                yield from HypergraphDepthBidirectionalCompartmentQuery. \
                    _depth_lookup_hierarchy(_current_cursor, self._parameters["lookup_name"],
                                            closed_set, 0, current_depth)
                closed_set.add(_current_cursor)
                _current_cursor = _current_cursor.parent
                current_depth += 1



