import abc

from enum import IntEnum


class EnumRegistryOperationResult(IntEnum):
    """
    Enumeration indicating the registry operation
    """

    CONFIRMED = 0
    DUPLICATE = -1
    EMPTY_REGISTRY = -2
    REGISTRY_LOOP = -3
    UNDEFINED_ERROR = -100


class ErrorRegisteredItemChangeAttempt(Exception):
    """
    Error that raised when a registered term attributes are changed illegally
    """


class ErrorRegistry(Exception):
    """
    Error raised through registry operation
    """


class MetaRegistrable(metaclass=abc.ABCMeta):
    """
    An interface indicating a registrable concept that can be registered as part
    of a medium-term or long-term memory
    """

    @abc.abstractmethod
    def __init__(self, name: str, timestamp: int):
        self.name = name
        self._registration_timestamp = timestamp
        self._uuid = None
        self._qualified_name: str = name
        # Indicate the registry where the registrable belongs
        self._parent_registry = None

    @property
    def uuid(self) -> bytes:
        """
        A unique id in the registry domain
        :return: ID in the bytestream form
        """
        return self._uuid

    @uuid.setter
    def uuid(self, arg: bytes) -> None:
        if self._uuid is None:
            self._uuid = arg
        else:
            raise ErrorRegisteredItemChangeAttempt

    @property
    def registration_timestamp(self) -> int:
        """
        Time of registration of item in integer format
        :return:
        """
        return self._registration_timestamp

    @registration_timestamp.setter
    def registration_timestamp(self, arg):
        """
        Setting timestamp is illegal
        """
        raise ErrorRegisteredItemChangeAttempt

    @property
    def qualified_name(self):
        """
        Qualified name inferred from registry hierarchy
        """
        return self._qualified_name

    @qualified_name.setter
    def qualified_name(self, arg):
        raise ErrorRegisteredItemChangeAttempt

    def set_parent(self, p):
        """
        Register the item into the argument registry

        :param p: a registry where to register the item
        :return:
        """
        self._parent_registry = p

    @abc.abstractmethod
    def register(self, registry, timestamp: int) -> None:
        """
        Register the term in a registry at a specific time

        :param registry: the registry to register the item
        :param timestamp: the time of registration
        :return: nothing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def deregister(self):
        raise NotImplementedError

    @abc.abstractmethod
    def reregister(self, new_registy, timestamp: int):
        raise NotImplementedError

    def update_qualified_name(self):
        if self._parent_registry is None:
            self._qualified_name = self.name
        else:
            self._qualified_name = '/'.join([self._parent_registry.qualified_name, self.name])



class MetaRegistry(MetaRegistrable):
    """
    Registry meta object
    """

    def __init__(self, name: str, timestamp: int):
        super().__init__(name, timestamp)


    @abc.abstractmethod
    def item_register(self, item: MetaRegistrable, timestamp: int) -> EnumRegistryOperationResult:
        """
        Register a registrable item in the registry

        :param item: the registrable item
        :param timestamp: the timestamp of registration
        :return: the result of registration (success or some error)
        """
        raise NotImplementedError

    @abc.abstractmethod
    def generate_domain_uid(self) -> bytes:
        """
        Generate a domain-specific unique id
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def item_deregister(self, item: MetaRegistrable) -> EnumRegistryOperationResult:
        """
        Deregister a concept object-wise (using local unique id)

        :param item: the item to be deregistered
        :return: the result of deregistration
        """
        raise NotImplementedError
