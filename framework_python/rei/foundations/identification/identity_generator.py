import abc
import hashlib

import typing


class MetaUniqueIdentifierGenerator(metaclass=abc.ABCMeta):

    def __init__(self, context_name: str, identity_generation: typing.Callable[[str, typing.Any], str]) -> None:
        super().__init__()
        self._context_name = context_name
        self._id_generation_function = identity_generation

    @abc.abstractmethod
    def generate_uid(self, arg) -> bytes:
        raise NotImplementedError


class Sha3UniqueIdentifierGenerator(MetaUniqueIdentifierGenerator):

    def __init__(self, context_name: str, identity_generation: typing.Callable[[str, typing.Any], str]) -> None:
        super().__init__(context_name, identity_generation)

    def generate_uid(self, arg) -> bytes:
        s = hashlib.sha3_224()
        s.update(self._id_generation_function(self._context_name, arg).encode("utf-8"))
        return s.digest()
