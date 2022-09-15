import asyncio
import copy
import math
import typing

import numpy as np

from rei.foundations.graph_monad import GraphVisitor
from rei.hypergraph.base_elements import HypergraphElement, HypergraphNode, HypergraphEdge, HypergraphRelation
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.homomorphism_functions import IndexHomomorphismGraphTensor
from rei.hypergraph.norm.norm_functions import NormFunctor


class HypergraphTraversal(GraphVisitor):

    def __init__(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                 filter_func: typing.Callable[[typing.Any], bool],
                 weight_func: NormFunctor, homomorphism: IndexHomomorphismGraphTensor = None,
                 depth=math.inf) -> None:
        super().__init__(visitor_func, filter_func)
        self._weight_function = weight_func
        self._index_homomorphism = homomorphism
        self.max_depth = depth

    def get_node_identification(self, el):
        if self._index_homomorphism is None:
            return map(lambda x: x.uuid, el.parent.induced_subset)
        return map(lambda x: self._index_homomorphism.node(x.uuid), el.parent.induced_subset)

    def get_edge_identification(self, el: HypergraphEdge):
        if self._index_homomorphism is None:
            return el.uuid
        return self._index_homomorphism.edge(el.uuid)

    async def __fill_edge(self, el: HypergraphEdge, _fringe, current_depth: int):
        for v in el.sub_relations:
            await _fringe.put((v, current_depth))
            _fringe.task_done()

    async def __fill_node(self, el: HypergraphNode, _fringe, current_depth: int):
        for v in el.sub_ports:
            print(v)
        for v in el.sub_edges:
            await _fringe.put((v, current_depth))
            _fringe.task_done()

    def __fill_relations(self, weight, endpoint_id, edge_id, norm_weight, el, task_list: list):
        if weight[0] != 0.0:
            task_list.append(asyncio.coroutine(
                self._visitor_func([(endpoint_id, x, edge_id, weight[0], norm_weight)
                                    for x in filter(lambda x: x is not endpoint_id,
                                                    self.get_node_identification(el))])))

        if weight[1] != 0.0:
            task_list.append(asyncio.coroutine(
                self._visitor_func([(x, endpoint_id, edge_id, weight[1], norm_weight)
                                    for x in filter(lambda x: x is not endpoint_id,
                                                    self.get_node_identification(el))])))


    async def _traverse(self, _fringe: asyncio.Queue, _task_list: list):
        if not _fringe.empty():
            _next, __current_depth = await _fringe.get()
            match _next:
                case HypergraphNode():
                    _next: HypergraphNode
                    await self.__fill_node(_next,_fringe, __current_depth)
                case HypergraphEdge():
                    _next: HypergraphEdge
                    await self.__fill_edge(_next, _fringe, __current_depth)
                case HypergraphRelation():
                    _next: HypergraphRelation
                    # Edge identification
                    edge_id = self.get_edge_identification(_next.parent)
                    # Weight normalization
                    norm_weight = np.array([1.0, 1.0])
                    if _next.weight is not None:
                        norm_weight = self._weight_function.norm(_next.weight.val)
                    else:
                        match _next.direction:
                            case EnumRelationDirection.BIDIRECTIONAL:
                                norm_weight = np.array([1.0, 1.0])
                            case EnumRelationDirection.INWARDS:
                                norm_weight = np.array([1.0, 0.0])
                            case EnumRelationDirection.OUTWARDS:
                                norm_weight = np.array([0.0, 1.0])
                    # TODO: t-norm
                    w = np.multiply(np.array(_next.relation_incidence_value), norm_weight)
                    # Endpoint identification
                    if self._index_homomorphism is None:
                        endpoint_id = _next.endpoint.uuid
                    else:
                        endpoint_id = self._index_homomorphism.node(_next.endpoint.uuid)
                    # Execute visitor func on pairs
                    self.__fill_relations(w, endpoint_id, edge_id, norm_weight, _next, _task_list)
                    # Add endpoints to fringe
                    if __current_depth + 1 < self.max_depth:
                        await _fringe.put((_next.endpoint, __current_depth + 1))
                        _fringe.task_done()
            await self._traverse(_fringe, _task_list)

    async def _setup(self, start: HypergraphElement, fringe: asyncio.Queue = asyncio.Queue()):
        _fringe = copy.copy(fringe)
        await _fringe.put((start, 0))
        _fringe.task_done()
        # Task list
        _task_list = []
        return _fringe, _task_list

    async def execute(self, start) -> list[asyncio.Future]:
        _fringe, _task_list = await self._setup(start)
        await self._traverse(_fringe, _task_list)
        return _task_list