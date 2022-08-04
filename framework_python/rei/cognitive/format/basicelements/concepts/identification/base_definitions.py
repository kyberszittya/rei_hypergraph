import abc
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
import copy


class ErrorIdentificationChangeAttempt(Exception):
    pass


class MetaIdentifiable(metaclass=abc.ABCMeta):
    """
    This interface indicates that an interface can be uniquely identified
    through unique id and timestamp.

    Unique ID is a generated using a hashing algorithm (e.g., SHA3-224).
    """


    @abc.abstractmethod
    def __init__(self, id_name: str, timestamp: int, identitygen: InterfaceIdentifierGenerator):
        self._uid: bytes | None = None
        self._identitygen: InterfaceIdentifierGenerator = identitygen
        self._timestamp: int = timestamp
        self._id_name: str = id_name

    @property
    def uid(self) -> bytes:
        if self._uid is None:
            self._uid = self._identitygen.generate_id(self._id_name, self._timestamp)
        return copy.copy(self._uid)

    @uid.setter
    def uid(self, arg):
        raise ErrorIdentificationChangeAttempt

    @property
    def identitygen(self):
        raise RuntimeError

    @identitygen.setter
    def identitygen(self, arg):
        raise RuntimeError

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, arg):
        raise ErrorIdentificationChangeAttempt

    @property
    def id_name(self):
        return self._id_name

    @id_name.setter
    def id_name(self, arg):
        """
        Shouldn't allow changing name

        :param arg:
        :return:
        """
        raise ErrorIdentificationChangeAttempt

    def reidentify(self, reg: InterfaceIdentifierGenerator) -> None:
        """
        Reregister element (e.g. if added as a part)
        :return:
        """
        self._uid = reg.generate_id(self._id_name, self._timestamp)
