import asyncio
import math

import typing
import copy
from abc import ABC

from rei.foundations.graph_monad import GraphVisitor
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge, HypergraphRelation
from rei.hypergraph.common_definitions import EnumRelationDirection


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
        if self._filter_func(start) and not self._ignore_root:
            _task_list.append(asyncio.coroutine(self._visitor_func(start)))
        return _fringe, _task_list

    async def _fill_visit_fringe(self, current_node, _fringe: asyncio.Queue, current_depth: int = 0):
        if current_depth < self._max_depth:
            for v in current_node.get_subelements(self._filter_func):
                await _fringe.put((v, current_depth + 1))
                _fringe.task_done()

    async def _traverse(self, _fringe, _task_list: list):
        if not _fringe.empty():
            _next, current_depth = await _fringe.get()
            await self._fill_visit_fringe(_next, _fringe, current_depth)
            # Add coroutine (TODO: seek for another solution to create coroutines)
            _task_list.append(asyncio.coroutine(self._visitor_func(_next)))
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

#
# SECTION: utility functions
#


def direction_to_text(direction: EnumRelationDirection):
    match direction:
        case EnumRelationDirection.OUTWARDS:
            return '->'
        case EnumRelationDirection.INWARDS:
            return '<-'
        case EnumRelationDirection.BIDIRECTIONAL:
            return '--'


def print_element(_el):
    match _el:
        case HypergraphNode():
            _el: HypergraphNode
            if _el.parent is None:
                print(f"node {_el.qualified_name}: {_el.id_name}")
            else:
                print(f"node {_el.qualified_name}: {_el.id_name} <- {_el.parent.id_name}")
        case HypergraphEdge():
            _el: HypergraphEdge
            print(f"edge {_el.qualified_name}: {_el.id_name} {_el.cnt_subelements} <- {_el.parent.id_name}")
        case HypergraphRelation():
            _el: HypergraphRelation
            print(f"relation {_el.qualified_name}: {direction_to_text(_el.direction)} {_el.endpoint.id_name}:: {_el.weight}")


async def print_graph_hierarchy(start):
    tr = BreadthFirstHierarchicalTraversal(lambda x: print_element(x), lambda x: True)
    return await tr.execute(start)