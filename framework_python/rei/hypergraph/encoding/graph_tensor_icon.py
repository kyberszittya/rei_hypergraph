import asyncio
import math
import queue

from rei.foundations.graph_monad import GraphMonad
from rei.foundations.hypergraph_traversal_strategies import HypergraphTraversal
from rei.hypergraph.base_elements import HypergraphNode, HypergraphRelation, HypergraphEdge
from rei.hypergraph.homomorphism_functions import IndexHomomorphismGraphTensor
from rei.hypergraph.norm.norm_functions import SumNorm
from rei.hypergraph.value_node import ValueNode


class CoordinateObjectTransformer(GraphMonad):

    def __init__(self, context: HypergraphNode, repr_depth: int = math.inf) -> None:
        super().__init__()
        self._index_homomorphism: IndexHomomorphismGraphTensor | None = None
        self.repr_depth = repr_depth
        self._context = context
        #
        self._msg_value_tensor = []
        self._msg_incidence_out = []
        self._msg_incidence_in = []
        # Value nodes
        self._msg_value_nodes = []
        self._msg_relations = []

    async def setup_homomorphism(self, context: HypergraphNode):
        self._index_homomorphism = IndexHomomorphismGraphTensor(True)

    async def reset(self, context: HypergraphNode):
        self._index_homomorphism = IndexHomomorphismGraphTensor(False, depth=math.inf)
        return await self._index_homomorphism.execute(context)

    def fill_tensors(self, i_e, i_n0, i_n1, i_w, val):
        self._msg_value_tensor.append((i_e, i_n1, i_n0, i_w))
        # Fill incidences
        self._msg_incidence_out.append((i_e, i_n1, i_w))
        self._msg_incidence_in.append((i_e, i_n0, i_w))

    async def execute(self, start: HypergraphNode | None = None) -> list[asyncio.Future]:
        if start is None:
            start = self._context
        q = queue.Queue()
        tr = HypergraphTraversal(
            lambda x: q.put(x), lambda x: True, SumNorm(), self._index_homomorphism, self.repr_depth)
        await tr.execute(start)
        while not q.empty():
            for v in q.get():
                i_n0, i_n1, i_e, i_w, val = v
                self.fill_tensors(i_e, i_n1, i_n0, i_w, val)

    def __msg_node_tuple(self, el: HypergraphNode):
        if el.parent is None:
            return el.uuid, el.id_name, self._index_homomorphism.node(el.uuid), 0, el.qualified_name.encode('utf-8')
        return el.uuid, el.id_name, self._index_homomorphism.node(el.uuid), el.parent.uuid, el.qualified_name.encode('utf-8')

    def __msg_edge_tuple(self, el: HypergraphEdge):
        return el.uuid, el.id_name, self._index_homomorphism.edge(el.uuid), el.parent.uuid, el.qualified_name

    def __msg_value_tuple(self, v: ValueNode):
        _val = v.get_values()
        return v.uuid, v.id_name, self._index_homomorphism.val(v.uuid), v.parent.uuid, _val

    def node_index_list(self):
        node_list = [self.__msg_node_tuple(self._context)]
        node_list.extend([self.__msg_node_tuple(i) for i in list(self._context.sub_nodes)])
        return node_list

    def edge_index_list(self):
        return [self.__msg_edge_tuple(i) for i in list(self._context.sub_edges)]

    def msg_relation_index_list(self):
        for el in map(lambda x: list(x.sub_relations), self._context.sub_edges):
            for rel in el:
                rel: HypergraphRelation
                self._msg_relations.append((rel.uuid, rel.id_name, "",
                                            rel.direction.value, rel.endpoint.uuid, rel.parent.uuid))
        return self._msg_relations

    def msg_value_updates(self):
        return self._msg_value_tensor, self._msg_incidence_out, self._msg_incidence_in

    def msg_value_nodes(self):
        return [self.__msg_value_tuple(v) for v in self._context.sub_values]

