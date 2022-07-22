import collections

from cognitive.format.basicelements.concepts.identification.base_definitions import MetaIdentifiable
from cognitive.format.basicelements.concepts.registry.registration_methods import \
    InterfaceIdentifierGenerator, IdentifierGeneratorSha224

from cognitive.format.basicelements.concepts.network.base_definitions import NetworkElement

import abc


class MetaHypergraphQuery(MetaIdentifiable):

    @abc.abstractmethod
    def __init__(self, cursor, id_name: str,
                 timestamp: int, identitygen: InterfaceIdentifierGenerator=None):
        if identitygen is None:
            super().__init__(id_name, timestamp, IdentifierGeneratorSha224(prefix=id_name))
        else:
            super().__init__(id_name, timestamp, identitygen)
        super().__init__(id_name, timestamp, identitygen)
        if cursor is not list or tuple:
            self._cursor: collections.Iterable[NetworkElement] = [cursor]
        else:
            self._cursor = cursor
        self._parameters: dict = {}

    def set_cursor_node(self, cursor: NetworkElement, timestamp: int):
        self._timestamp = timestamp
        self._cursor: list[NetworkElement] = [cursor]

    def add_parameter(self, id: str, arg):
        self._parameters[id] = arg

    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError



