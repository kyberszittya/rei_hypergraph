import abc
import typing

from rei.foundations.abstract_items import IdentifiableItem
from rei.foundations.clock import MetaClock
from rei.foundations.common_errors import ErrorDuplicateElement, InvalidQueryName, ErrorClockNotSet, \
    ErrorRecursiveHierarchy, ErrorInvalidQuery


class InterfaceSetElement(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_element(self, element) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_element(self, id_name: str = "", uuid: bytes = None) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError


class HierarchicalElement(IdentifiableItem, InterfaceSetElement):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent=None) -> None:
        super().__init__(uuid, id_name, progenitor_qualified_name)
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, arg):
        self._parent = arg

    @abc.abstractmethod
    def get_element_by_id_name(self, id_name: str) -> typing.Generator:
        raise NotImplementedError

    def update_qualified_name(self):
        yield self._id_name
        if self._parent is not None:
            yield from self._parent.update_qualified_name()


class ConceptualItem(HierarchicalElement):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str,
                 clock: MetaClock, parent: HierarchicalElement = None) -> None:
        super().__init__(uuid, id_name, qualified_name, parent)
        self._clock = clock
        # Subelement count
        self._cnt_subelements = 0
        self._cnt_subelements_historical = self._cnt_subelements
        # Context related attributes
        self._cid = 0
        self._sub_elements = {}
        # Indices
        self._index_elements_by_name = {}
        # Timestamp
        self._update_timestamp()
        # Setup parent
        if parent is not None:
            parent.add_element(self)

    @property
    def clock(self):
        return self._clock

    @clock.setter
    def clock(self, arg: MetaClock):
        self._clock = arg

    @property
    def cnt_subelements(self):
        return self._cnt_subelements

    @property
    def cid(self):
        return self._cid

    @cid.setter
    def cid(self, arg: int):
        self._cid = arg

    @property
    def timestamp(self):
        return self._timestamp

    def _update_timestamp(self):
        if self._clock is not None:
            self._timestamp = self._clock.get_time_ns()
        else:
            raise ErrorClockNotSet

    def add_element(self, element: HierarchicalElement):
        # Forbid hierarchy recursion
        if element is self:
            raise ErrorRecursiveHierarchy
        # Add as unique element
        if element.uuid not in self._sub_elements:
            self._sub_elements[element.uuid] = element
        else:
            raise ErrorDuplicateElement
        # Index by names (multiple names can exist, add them as a list)
        if element.id_name not in self._index_elements_by_name:
            self._index_elements_by_name[element.id_name] = {}
        self._index_elements_by_name[element.id_name][element.uuid] = element
        # Set the CID of the added element
        element.cid = self._cnt_subelements_historical
        # Set the parent of the element
        element.parent = self
        # Subelement count increment
        self._cnt_subelements += 1
        #
        self._cnt_subelements_historical += 1
        # Update timestamp
        element.update()

    def remove_element(self, id_name: str = "", uuid: bytes = None) -> None:
        if len(id_name) > 0:
            if uuid is not None:
                el = self._sub_elements.pop(uuid)
                self._index_elements_by_name[id_name].pop(uuid)
                # Invalidate parent
                el.parent = None
                el.update()
                # Decrement element count
                self._cnt_subelements -= 1
            else:
                for v in self._index_elements_by_name[id_name].values():
                    el = self._sub_elements.pop(v.uuid)
                    # Invalidate each element parent
                    el.parent = None
                    # Update timestamp etc.
                    el.update()
                    # Decrement by each element
                    self._cnt_subelements -= 1
                self._index_elements_by_name[id_name] = {}
        else:
            if uuid is not None:
                el = self._sub_elements.pop(uuid)
                self._index_elements_by_name[el.id_name].pop(uuid)
                # Invalidate element parent
                el.parent = None
                # Update tiemstamp etc.
                el.update()
                # Decrement element
                self._cnt_subelements -= 1
            else:
                raise ErrorInvalidQuery

    def get_element_by_id_name(self, id_name: str) -> typing.Generator:
        tokens = id_name.split('/')
        if len(tokens) == 0:
            raise InvalidQueryName
        elif len(tokens) == 1:
            if tokens[0] in self._index_elements_by_name:
                yield from list(self._index_elements_by_name[tokens[0]].values())
            else:
                yield from []
        else:
            # Iterate all possible named elements
            for v in self._index_elements_by_name[tokens[0]].values():
                yield from v.get_element_by_id_name('/'.join(tokens[1:]))

    def get_subelements(self, filterfunc: typing.Callable[[object], bool]) -> typing.Generator:
        yield from filter(filterfunc, self._sub_elements.values())

    def update(self):
        self._update_timestamp()
        self._qualified_name = '/'.join(list(self.update_qualified_name())[::-1])
