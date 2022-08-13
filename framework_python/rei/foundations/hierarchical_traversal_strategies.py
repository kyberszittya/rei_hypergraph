import asyncio
import math

import typing
import copy
from abc import ABC

from rei.foundations.graph_monad import GraphVisitor


class HierarchicalTraversal(GraphVisitor, ABC):

    def __init__(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                 filter_func: typing.Callable[[typing.Any], bool], ignore_root: bool = False) -> None:
        super().__init__(visitor_func, filter_func)
        self._max_depth = math.inf
        self._ignore_root = ignore_root

    async def _setup_visit_algorithm(self, start: typing.Any,
                                     fringe: asyncio.Queue = asyncio.Queue()) \
            -> tuple[asyncio.Queue | asyncio.LifoQueue, list]:
        # Fringe setup
        _fringe = copy.copy(fringe)
        # Task list setup
        _task_list = []
        if self.filter_func(start) and not self._ignore_root:
            _task_list.append(asyncio.coroutine(self.visitor_func(start)))
        return _fringe, _task_list

    async def _fill_visit_fringe(self, current_node, _fringe: asyncio.Queue, current_depth: int = 0):
        if current_depth < self._max_depth:
            for v in current_node.get_subelements(self.filter_func):
                await _fringe.put((v, current_depth + 1))
                _fringe.task_done()

    async def _traverse(self, _fringe, _task_list: list):
        if not _fringe.empty():
            _next, current_depth = await _fringe.get()
            await self._fill_visit_fringe(_next, _fringe, current_depth)
            # Add coroutine (TODO: seek for another solution to create coroutines)
            _task_list.append(asyncio.coroutine(self.visitor_func(_next)))
            await self._traverse(_fringe, _task_list)


class BreadthFirstHierarchicalTraversal(HierarchicalTraversal):

    async def execute(self, start) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup_visit_algorithm(start)
        await self._fill_visit_fringe(start, _fringe)
        await self._traverse(_fringe, _task_list)
        return _task_list


class DepthFirstHierarchicalTraversal(HierarchicalTraversal):

    async def execute(self, start) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup_visit_algorithm(start, asyncio.LifoQueue())
        await self._fill_visit_fringe(start, _fringe)
        await self._traverse(_fringe, _task_list)
        return _task_list


class DepthLimitedDepthVisitChildren(HierarchicalTraversal):

    def __init__(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                 filter_func: typing.Callable[[typing.Any], bool], max_depth: int, ignore_root: bool = False) -> None:
        super().__init__(visitor_func, filter_func, ignore_root)
        self._max_depth = max_depth

    async def execute(self, start) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup_visit_algorithm(start, asyncio.LifoQueue())
        await self._fill_visit_fringe(start, _fringe, 0)
        await self._traverse(_fringe, _task_list)
        return _task_list


class DepthLimitedBreadthVisitChildren(HierarchicalTraversal):

    def __init__(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                 filter_func: typing.Callable[[typing.Any], bool], max_depth: int, ignore_root: bool = False) -> None:
        super().__init__(visitor_func, filter_func, ignore_root)
        self._max_depth = max_depth

    async def execute(self, start) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup_visit_algorithm(start)
        await self._fill_visit_fringe(start, _fringe, 0)
        await self._traverse(_fringe, _task_list)
        return _task_list
