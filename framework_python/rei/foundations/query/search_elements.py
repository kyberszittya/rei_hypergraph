import abc
import asyncio
import typing
from abc import ABC
import copy

from rei.foundations.graph_monad import GraphMonad
from rei.hypergraph.base_elements import HypergraphNode, HypergraphElement


class GraphQuery(GraphMonad, ABC):

    def __init__(self) -> None:
        super().__init__()
        self._query_def = ""
        self._result = []
        self._element_cache = {}

    def _setup_query(self, fringe: asyncio.Queue = asyncio.Queue()):
        _fringe = copy.copy(fringe)
        _task_list = []
        return _fringe, _task_list

    @property
    def query_def(self):
        return self._query_def

    @query_def.setter
    def query_def(self, arg):
        self._query_def = arg

    @property
    def query_result(self):
        return self._result

    @abc.abstractmethod
    async def _traverse(self, fringe: asyncio.Queue):
        raise NotImplementedError

    async def execute(self, start: HypergraphNode) -> list[asyncio.Future]:
        self._result = []
        if self.query_def in self._element_cache:
            self._result = [self._element_cache[self.query_def]]
            return []
        __fringe, _task_list = self._setup_query()
        await __fringe.put(start)
        __fringe.task_done()
        await self._traverse(__fringe)
        return []


class QuerySearchSubElement(GraphQuery):

    def __init__(self):
        super().__init__()

    async def _traverse(self, fringe: asyncio.Queue):
        if not fringe.empty():
            __next: HypergraphElement = await fringe.get()
            if __next.qualified_name == self._query_def:
                self._element_cache[__next.qualified_name] = __next
                self._result.append(__next)
                return
            for n in __next.get_subelements(lambda x: True):
                await fringe.put(n)
                fringe.task_done()
            await self._traverse(fringe)


class QuerySearchElement(GraphQuery):

    def __init__(self):
        super().__init__()
        self.visited_set = set()

    async def _traverse(self, fringe: asyncio.Queue):
        if not fringe.empty():
            __next: HypergraphElement = await fringe.get()
            if __next.parent is not None:
                await fringe.put(__next.parent)
                self.visited_set.add(__next.uuid)
                fringe.task_done()
            if __next.qualified_name == self._query_def:
                self._element_cache[__next.qualified_name] = __next
                self._result.append(__next)
                return
            for n in __next.get_subelements(lambda x: True):
                # TODO: exclude same elements
                #if n.uuid not in self.visited_set:
                await fringe.put(n)
                fringe.task_done()
            await self._traverse(fringe)

    async def execute(self, start: HypergraphNode) -> list[asyncio.Future]:
        self.visited_set = set()
        return await super().execute(start)


