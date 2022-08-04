import abc

from rei.cognitive.format.basicelements.concepts.identification.base_definitions import MetaIdentifiable
from rei.cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistrable
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator, \
    IdentifierGeneratorSha224


class FragmentMessage(MetaIdentifiable):

    def __init__(self, id_name: str, timestamp: int, identitygen: InterfaceIdentifierGenerator):
        super().__init__(id_name, timestamp, identitygen)

    @abc.abstractmethod
    def serialize_bytes(self) -> bytes:
        raise NotImplementedError
