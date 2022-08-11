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
        self._parent = parent
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

    @property
    def cid(self):
        return self._cid

    @cid.setter
    def cid(self, arg: int):
        self._cid = arg

    def get_subelements(self, filterfunc: typing.Callable[[typing.Any], bool]) -> typing.Generator:
        yield from filter(filterfunc, self._sub_elements.values())

    async def breadth_visit_children(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                                     filter_func: typing.Callable[[typing.Any], bool],
                                     task_list: list = None,
                                     fringe: asyncio.Queue = None) -> list[asyncio.Future]:
        # Fringe setup
        if fringe is None:
            _fringe = asyncio.Queue()
            await _fringe.put(self)
            _fringe.task_done()
        else:
            _fringe = fringe
        # Task list setup
        if task_list is None:
            _task_list = []
            if filter_func(self):
                _task_list.append(asyncio.coroutine(visitor_func(self)))
        else:
            _task_list = task_list
        # Start processing
        if not _fringe.empty():
            _next = await _fringe.get()
            for v in _next.get_subelements(filter_func):
                await _fringe.put(v)
                _fringe.task_done()
                # Add coroutine (TODO: seek for another solution to create coroutines)
                _task_list.append(asyncio.coroutine(visitor_func(v)))
            await _next.breadth_visit_children(visitor_func, filter_func, _task_list, _fringe)
            return _task_list

    async def depth_visit_children(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                                   filter_func: typing.Callable[[typing.Any], bool],
                                   task_list: list = None,
                                   fringe: asyncio.LifoQueue = None) -> list[asyncio.Future]:
        # Fringe
        if fringe is None:
            _fringe = asyncio.LifoQueue()
            await _fringe.put(self)
            _fringe.task_done()
        else:
            _fringe = fringe
        # Task list setup
        if task_list is None:
            _task_list = []
            if filter_func(self):
                _task_list.append(asyncio.coroutine(visitor_func(self)))
        else:
            _task_list = task_list
        # Start processing
        if not _fringe.empty():
            _next = await _fringe.get()
            for v in _next.get_subelements(filter_func):
                await _fringe.put(v)
                _fringe.task_done()
                _task_list.append(asyncio.coroutine(visitor_func(v)))
            await _next.depth_visit_children(visitor_func, filter_func, _task_list, _fringe)
            return _task_list


class InterfaceNamedSubelements(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_element_by_id_name(self, id_name: str) -> typing.Generator:
        raise NotImplementedError


class ConceptualItem(HierarchicalElement, InterfaceSetMultipleElementsOperation, InterfaceNamedSubelements):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str,
                 clock: MetaClock, parent: HierarchicalElement = None) -> None:
        super().__init__(uuid, id_name, qualified_name, parent)
        self._clock = clock
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
        if element.parent is not self:
            element.parent = self
        # Subelement count increment
        self._cnt_subelements += 1
        #
        self._cnt_subelements_historical += 1
        # Update timestamp
        element.update()

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
