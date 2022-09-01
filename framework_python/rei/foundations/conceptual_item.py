import abc
import asyncio
import typing
from abc import ABC

from rei.foundations.abstract_items import IdentifiableItem
from rei.foundations.clock import MetaClock
from rei.foundations.common_errors import ErrorDuplicateElement, InvalidQueryName, ErrorClockNotSet, \
    ErrorRecursiveHierarchy, ErrorInvalidQuery


class InterfaceSetOperations(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_element(self, element) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_element(self, id_name: str = "", uuid: bytes = None) -> typing.Generator:
        raise NotImplementedError


class InterfaceSetMultipleElementsOperation(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def add_elements(self, elements: typing.Iterable[typing.Any]) -> asyncio.Future:
        raise NotImplementedError

    @abc.abstractmethod
    async def remove_elements(self, elements: typing.Iterable[tuple[str, bytes]]) -> asyncio.Future:
        raise NotImplementedError


class HierarchicalElement(IdentifiableItem, InterfaceSetOperations, ABC):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent=None) -> None:
        super().__init__(uuid, id_name, progenitor_qualified_name)
        self._parent = None
        # Context related attributes
        self._cid = 0
        #
        # Subelements
        #
        # Subelement count
        self._cnt_subelements = 0
        # All subelements assigned to this element
        self._cnt_subelements_historical = self._cnt_subelements
        # All subelements
        self._sub_elements = {}
        # Indices
        self._index_elements_by_name = {}

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, arg):
        self._parent = arg

    def update_qualified_name(self):
        yield self._id_name
        if self._parent is not None:
            yield from self._parent.update_qualified_name()

    def update(self):
        self._qualified_name = '/'.join(list(self.update_qualified_name())[::-1])

    @property
    def cid(self):
        return self._cid

    @cid.setter
    def cid(self, arg: int):
        self._cid = arg

    def get_subelements(self, filterfunc: typing.Callable[[typing.Any], bool]) -> typing.Generator:
        yield from filter(filterfunc, self._sub_elements.values())

    def add_element(self, element):
        # Forbid hierarchy recursion
        if element is self:
            raise ErrorRecursiveHierarchy
        # Add as unique element
        if element.uuid not in self._sub_elements:
            self._sub_elements[element.uuid] = element
        else:
            raise ErrorDuplicateElement
        # Set the parent of the element
        if element.parent is not self:
            # Index by names (multiple names can exist, add them as a list)
            if element.id_name not in self._index_elements_by_name:
                self._index_elements_by_name[element.id_name] = {}
            self._index_elements_by_name[element.id_name][element.uuid] = element
            # Set the CID of the added element
            element.cid = self._cnt_subelements_historical
            # Check whether this element has been assigned to somewhere else
            if element.parent is not None:
                for e in element.parent.remove_element(uuid=element.uuid):            # Update all sub elements
                    e.update()
            element.parent = self
            # Subelement count increment
            self._cnt_subelements += 1
            # All-ever created subelement count
            self._cnt_subelements_historical += 1
            # Update subelements as well
            self.__update_element(element)

    def remove_element(self, id_name: str = "", uuid: bytes = None) -> typing.Generator:
        if len(id_name) > 0:
            if uuid is not None:
                el = self._sub_elements.pop(uuid)
                self._index_elements_by_name[id_name].pop(uuid)
                # Invalidate parent
                el.parent = None
                el.update()
                # Decrement element count
                self._cnt_subelements -= 1
                # Yield element
                yield el
            else:
                __tmp = [x for x in self._index_elements_by_name[id_name].values()]
                # Reset indices
                self._index_elements_by_name[id_name] = {}
                for v in __tmp:
                    el = self._sub_elements.pop(v.uuid)
                    # Invalidate each element parent
                    el.parent = None
                    # Update timestamp etc.
                    el.update()
                    # Decrement by each element
                    self._cnt_subelements -= 1
                    # Yield element
                    yield el
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
                # Yield element
                yield el
            else:
                raise ErrorInvalidQuery

    def __update_element(self, element):
        import queue
        __fringe = queue.Queue()
        __fringe.put(element)
        while not __fringe.empty():
            __next: HierarchicalElement = __fringe.get()
            __next.update()
            for e in __next.get_subelements(lambda x: True):
                __fringe.put(e)


class InterfaceNamedSubelements(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_element_by_id_name(self, id_name: str) -> typing.Generator:
        raise NotImplementedError


class ConceptualItem(HierarchicalElement, InterfaceSetMultipleElementsOperation, InterfaceNamedSubelements):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str,
                 clock: MetaClock, parent: HierarchicalElement = None) -> None:
        super().__init__(uuid, id_name, qualified_name, parent)
        self._clock = clock

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
    def timestamp(self):
        return self._timestamp

    def _update_timestamp(self):
        if self._clock is not None:
            self._timestamp = self._clock.get_time_ns()
        else:
            raise ErrorClockNotSet



    async def add_elements(self, elements: typing.Iterable[typing.Any]) -> asyncio.Future:
        return asyncio.gather(self.add_element(x) for x in elements)

    async def remove_elements(self, elements: typing.Iterable[tuple[str, bytes]]) -> asyncio.Future:
        return asyncio.gather(*[self.remove_element(e[0], e[1]) for e in elements])

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

    def update(self):
        self._update_timestamp()
        self._qualified_name = '/'.join(list(self.update_qualified_name())[::-1])
