import typing

from rei.foundations.clock import MetaClock
from rei.foundations.conceptual_item import HierarchicalElement
from rei.foundations.graph_monad import GraphMonad
from rei.foundations.hierarchical_traversal_strategies import BreadthFirstHierarchicalTraversal
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge, HypergraphRelation

import asyncio

from rei.hypergraph.value_node import SemanticValueNode


class HierarchicalPrepositionQuery(GraphMonad):

    def __init__(self, context: HypergraphNode, prep: typing.Callable[[typing.Any], bool],
                 traversal_statement: typing.Callable[[typing.Any], bool]):
        super().__init__()
        self.__preposition = prep
        # Context
        self.__start = context
        # Query handling
        self.__result = asyncio.Queue()
        self.__prefilter = []
        self.__bfs = BreadthFirstHierarchicalTraversal(lambda x: self.__prefilter.append(self.add_to_result(x)),
                                                       lambda x: isinstance(x, HypergraphNode | HypergraphRelation |
                                                                            HypergraphEdge | SemanticValueNode) and traversal_statement(x))

    async def prefilter(self):
        await self.__bfs.execute(self.__start)
        return self.__prefilter

    async def add_to_result(self, x):
        if self.__preposition(x):
            await self.__result.put(x)
            self.__result.task_done()

    async def execute(self, x=None):
        while not self.__result.empty():
            yield await self.__result.get()

    async def get_list_results(self):
        res = []
        async for e in self.execute():
            res.append(e)
        return res


class HypergraphQueryEngine(HypergraphNode):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None) -> None:
        super().__init__(id_name, uuid, qualified_name, clock, parent)
        self.__queries = dict()

    def add_query(self, name: str, query):
        self.__queries[name] = query

    def clear(self):
        self.__queries = dict()

    def prefilter_queries(self):
        task_list = []
        for e in self.__queries.values():
            task_list.append(e.prefilter())
        return task_list

    async def task_result_queries_lists(self):
        task_list = []
        for e in self.__queries.values():
            task_list.append(e.get_list_results())
        return task_list

    async def execute(self):
        __tasks = []
        prefilter = self.prefilter_queries()
        for i in prefilter:
            __tasks.extend(await i)
        await asyncio.wait(__tasks)
        res = []
        __task_list = await self.task_result_queries_lists()
        for t in __task_list:
            res.extend(await t)
        return res

    def execute_all_queries(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = []
        for i in self.prefilter_queries():
            tasks.extend(loop.run_until_complete(i))
        loop.run_until_complete(asyncio.wait(tasks))
        results = []
        for i in self.__queries.values():
            results.extend(loop.run_until_complete(i.get_list_results()))
        return results
