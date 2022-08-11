import asyncio
import math

import typing
import copy

from rei.foundations.graph_monad import GraphMonad


class HierarchicalTraversal(GraphMonad):



    def __init__(self) -> None:
        super().__init__()
        self.max_depth = math.inf

    @staticmethod
    async def _setup_visit_algorithm(start: typing.Any,
                                     visitor_func: typing.Callable[[typing.Any], typing.Any],
                                     filter_func: typing.Callable[[typing.Any], bool],
                                     fringe: asyncio.Queue = asyncio.Queue()) -> tuple[asyncio.Queue|asyncio.LifoQueue, list]:
        # Fringe setup
        _fringe = copy.copy(fringe)
        # Task list setup
        _task_list = []
        if filter_func(start):
            _task_list.append(asyncio.coroutine(visitor_func(start)))
        return _fringe, _task_list

    async def _fill_visit_fringe(self, current_node, _fringe: asyncio.Queue,
                                 filter_func: typing.Callable[[typing.Any], bool],
                                 current_depth: int = 0):
        if current_depth < self.max_depth:
            for v in current_node.get_subelements(filter_func):
                await _fringe.put((v, current_depth + 1))
                _fringe.task_done()

    async def _traverse(self, _fringe, visitor_func: typing.Callable[[typing.Any], typing.Any],
                        filter_func: typing.Callable[[typing.Any], bool], _task_list: list):
        if not _fringe.empty():
            _next, current_depth = await _fringe.get()
            await self._fill_visit_fringe(_next, _fringe, filter_func, current_depth)
            # Add coroutine (TODO: seek for another solution to create coroutines)
            _task_list.append(asyncio.coroutine(visitor_func(_next)))
            await self._traverse(_fringe, visitor_func, filter_func, _task_list)


class BreadthFirstHierarchicalTraversal(HierarchicalTraversal):

    async def execute(self, start, visitor_func: typing.Callable[[typing.Any], typing.Any],
                      filter_func: typing.Callable[[typing.Any], bool]) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup_visit_algorithm(start, visitor_func, filter_func)
        await self._fill_visit_fringe(start, _fringe, filter_func)
        await self._traverse(_fringe, visitor_func, filter_func, _task_list)
        return _task_list


class DepthFirstHierarchicalTraversal(HierarchicalTraversal):
    
    async def execute(self, start, visitor_func: typing.Callable[[typing.Any], typing.Any],
                                   filter_func: typing.Callable[[typing.Any], bool]) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup_visit_algorithm(start, visitor_func, filter_func, asyncio.LifoQueue())
        await self._fill_visit_fringe(start, _fringe, filter_func)
        await self._traverse(_fringe, visitor_func, filter_func, _task_list)
        return _task_list


class DepthLimitedDepthVisitChildren(HierarchicalTraversal):

    def __init__(self, max_depth: int) -> None:
        super().__init__()
        self.max_depth = max_depth

    async def execute(self, start, visitor_func: typing.Callable[[typing.Any], typing.Any],
                      filter_func: typing.Callable[[typing.Any], bool]) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup_visit_algorithm(start, visitor_func, filter_func, asyncio.LifoQueue())
        await self._fill_visit_fringe(start, _fringe, filter_func, 0)
        await self._traverse(_fringe, visitor_func, filter_func, _task_list)
        return _task_list


class DepthLimitedBreadthVisitChildren(HierarchicalTraversal):

    def __init__(self, max_depth: int) -> None:
        super().__init__()
        self.max_depth = max_depth

    async def execute(self, start, visitor_func: typing.Callable[[typing.Any], typing.Any],
                      filter_func: typing.Callable[[typing.Any], bool]) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup_visit_algorithm(start, visitor_func, filter_func)
        await self._fill_visit_fringe(start, _fringe, filter_func, 0)
        await self._traverse(_fringe, visitor_func, filter_func, _task_list)
        return _task_list
