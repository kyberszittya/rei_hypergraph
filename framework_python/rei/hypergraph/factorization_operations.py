import asyncio
import typing

from rei.foundations.graph_monad import GraphMonad
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge


class Factorization2Operation(GraphMonad):

    def __init__(self) -> None:
        super().__init__()
        self.__relation_list = []

    async def __traverse(self, fringe: asyncio.Queue):
        if not fringe.empty():
            __next = await fringe.get()
            match __next:
                case HypergraphNode():
                    __next: HypergraphNode
                    for e in __next.sub_edges:
                        await fringe.put(e)
                        fringe.task_done()
                case HypergraphEdge():
                    __next: HypergraphEdge
                    i_e = __next.get_incoming_relations()
                    o_e = __next.get_outgoing_relations()
                    for i in i_e:
                        self.__relation_list.append((i, list(__next.get_outgoing_relations())))
                    for i in o_e:
                        await fringe.put(i.endpoint)
                        fringe.task_done()
            await self.__traverse(fringe)
        else:
            return

    async def execute(self, start) -> list[asyncio.Future]:
        self.__relation_list = []
        __fringe = asyncio.Queue()
        await __fringe.put(start)
        __fringe.task_done()
        await self.__traverse(__fringe)
        return self.__relation_list


class MapFactorizationToFactorGraph(GraphMonad):

    def __init__(self, mapping_function: typing.Callable[[typing.Any], typing.Any]) -> None:
        super().__init__()
        self.__mapping_function = mapping_function

    async def execute(self, start) -> map:
        return map(lambda x: self.__mapping_function(x), start)

