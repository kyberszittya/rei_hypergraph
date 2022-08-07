import abc
import hashlib
import typing

from rei.arbiter.hypergraph_arbiter import HypergraphNode
from rei.foundations.clock import MetaClock


class MetaUniqueIdentifierGenerator(metaclass=abc.ABCMeta):

    def __init__(self, context_name: str, identity_generation: typing.Callable[[str, object], str]) -> None:
        super().__init__()
        self._context_name = context_name
        self._id_generation_function = identity_generation

    @abc.abstractmethod
    def generate_uid(self, arg) -> bytes:
        raise NotImplementedError


class Sha3UniqueIdentifierGenerator(MetaUniqueIdentifierGenerator):

    def __init__(self, context_name: str, identity_generation: typing.Callable[[str, object], str]) -> None:
        super().__init__(context_name, identity_generation)

    def generate_uid(self, arg) -> bytes:
        s = hashlib.sha3_224()
        s.update(self._id_generation_function(self._context_name, arg).encode("utf-8"))
        return s.digest()


class HypergraphFactory():

    def __init__(self, factory_name: str, clock: MetaClock) -> None:
        super().__init__()
        self._factory_name: str = factory_name
        self._clock: MetaClock = clock
        self.unique_identifier = Sha3UniqueIdentifierGenerator(
            self._factory_name, lambda x, y: f"{x}.{self.get_qualified_name(y.id_name)}")

    def get_qualified_name(self, name: str):
        return f"{name}.{self._clock.get_time_ns()}"

    def generate_node(self, id_name: str):
        node = HypergraphNode()
