import asyncio
import copy
import math
import typing

from rei.foundations.graph_monad import GraphVisitor
from rei.hypergraph.base_elements import HypergraphElement, HypergraphNode, HypergraphEdge, HypergraphRelation
from rei.hypergraph.value_node import ValueNode


class HypergraphTraversal(GraphVisitor):

    def __init__(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                 filter_func: typing.Callable[[typing.Any], bool],
                 weight_func: typing.Callable[[ValueNode], float],
                 depth=math.inf) -> None:
        super().__init__(visitor_func, filter_func)
        self._weight_function = weight_func
        self.max_depth = depth

    async def _traverse(self, _fringe: asyncio.Queue, task_list: list):
        _next = await _fringe.get()
        match _next:
            case HypergraphNode():
                _next: HypergraphNode
                for v in _next.sub_ports:
                    print(v)
            case HypergraphEdge():
                _next: HypergraphEdge
                for v in _next.sub_relations:
                    v: HypergraphRelation
                    self._weight_function(v.weight)
                    weight = 1.0
                    if v.weight is not None:
                        weight = self._weight_function(v.weight.val)
                    print(v.relation_incidence_value, weight)


    async def _setup(self, start: HypergraphElement, fringe: asyncio.Queue = asyncio.Queue()):
        _fringe = copy.copy(fringe)
        _task_list = []
        await _fringe.put(start)
        _fringe.task_done()
        return _fringe, _task_list

    async def execute(self, start) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup(start)
        await self._traverse(_fringe, _task_list)