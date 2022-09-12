import asyncio
import typing

from rei.foundations.graph_monad import GraphMonad
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge, HypergraphRelation
from rei.hypergraph.common_definitions import EnumRelationDirection


class Factorization2Operation(GraphMonad):

    def __init__(self):
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


class Factorization2SubsetOperation(GraphMonad):

    def __init__(self, self_loop=False):
        super().__init__()
        self.nodes = None
        self.self_loop = self_loop

    async def execute(self, start) -> list[asyncio.Future]:
        self.__relation_list = []
        self.nodes = [x for x in filter(lambda x: isinstance(x, HypergraphNode), start)]
        for __edge in filter(lambda x: isinstance(x, HypergraphEdge), start):
            __edge: HypergraphEdge
            i_e = filter(lambda x: x.endpoint in self.nodes, __edge.get_incoming_relations())
            for e in i_e:
                o_e = filter(lambda x: x.endpoint in self.nodes, __edge.get_outgoing_relations())
                for e1 in o_e:
                    if (e.endpoint.uuid != e1.endpoint.uuid) or self.self_loop:
                        self.__relation_list.append([e, e1])
        return self.__relation_list


class RelationFactorization2SubsetOperation(GraphMonad):

    def __init__(self, self_loop=False):
        super().__init__()
        self.nodes = None
        self.self_loop = self_loop

    async def execute(self, start) -> list[asyncio.Future]:
        self.__relation_list = []
        self.nodes = [x for x in filter(lambda x: isinstance(x, HypergraphNode), start)]
        self.incoming_relations = {}
        self.outgoing_relations = {}
        # Collect incoming and outgoing edges
        for __rel in filter(lambda x: isinstance(x, HypergraphRelation), start):
            __rel: HypergraphRelation
            if __rel.direction == EnumRelationDirection.INWARDS or __rel.direction == EnumRelationDirection.BIDIRECTIONAL:
                if __rel.parent.uuid not in self.incoming_relations:
                    self.incoming_relations[__rel.parent.uuid] = []
                self.incoming_relations[__rel.parent.uuid].append(__rel)
            elif __rel.direction == EnumRelationDirection.OUTWARDS:
                if __rel.parent.uuid not in self.outgoing_relations:
                    self.outgoing_relations[__rel.parent.uuid] = []
                self.outgoing_relations[__rel.parent.uuid].append(__rel)
        # Pair relations
        for k in self.incoming_relations:
            for i_e in self.incoming_relations[k]:
                for o_e in self.outgoing_relations[k]:
                    if (o_e.endpoint.uuid != i_e.endpoint.uuid) or self.self_loop:
                        self.__relation_list.append([i_e, o_e])
        # Relation list
        return self.__relation_list


class MapFactorizationToFactorGraph(GraphMonad):

    def __init__(self, mapping_function: typing.Callable[[typing.Any], typing.Any]) -> None:
        super().__init__()
        self.__mapping_function = mapping_function

    async def execute(self, start) -> map:
        return map(lambda x: self.__mapping_function(x), start)

