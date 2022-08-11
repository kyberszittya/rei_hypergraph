import abc


class IdentifiableItem(metaclass=abc.ABCMeta):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str) -> None:
        super().__init__()
        self._uuid = uuid
        self._id_name = id_name
        self._progenitor_qualified_name = progenitor_qualified_name
        # Qualified name
        self._qualified_name = id_name

    @property
    def id_name(self):
        return self._id_name

    @property
    def uuid(self):
        return self._uuid

    @property
    def progenitor_qualified_name(self):
        return self._progenitor_qualified_name

    @property
    def qualifed_name(self):
        return self._qualified_name

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError
