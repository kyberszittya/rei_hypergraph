import asyncio
import typing

from rei.foundations.graph_monad import GraphMonad
from rei.foundations.hierarchical_traversal_strategies import DepthLimitedBreadthVisitChildren, HierarchicalTraversal
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge


class IndexHomomorphismGraphTensor(GraphMonad):

    def __init__(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                 filter_func: typing.Callable[[typing.Any], bool], depth: int = 1):
        super().__init__(visitor_func, filter_func)
        # Counts
        self.cnt_node = 0
        self.cnt_edges = 0
        # Homology dictionaries
        self.__hom_node_dim: dict[bytes, int] = {}
        self.__hom_edge_depth: dict[bytes, int] = {}
        self.__hom_dim_node: dict[int, bytes] = {}
        self.__hom_depth_edge: dict[int, bytes] = {}
        # Depth of mapping
        self._depth = depth
        # Traversals
        self.edges_bfs: HierarchicalTraversal = DepthLimitedBreadthVisitChildren(
            self.add_edge_homology, lambda x: isinstance(x, HypergraphEdge), self._depth)
        self.nodes_bfs: HierarchicalTraversal = DepthLimitedBreadthVisitChildren(
            self.add_node_homology, lambda x: isinstance(x, HypergraphNode), self._depth)

    def add_edge_homology(self, arg: HypergraphEdge):
        # Edges homology
        self.__hom_edge_depth[arg.uuid] = self.cnt_edges
        self.__hom_depth_edge[self.cnt_edges] = arg.uuid
        # Increment edge count
        self.cnt_edges += 1

    def add_node_homology(self, arg: HypergraphNode):
        # Node homology
        # TODO: atomics
        self.__hom_node_dim[arg.uuid] = self.cnt_node
        self.__hom_dim_node[self.cnt_node] = arg.uuid
        # Increment node count
        self.cnt_node += 1

    async def execute(self, start) -> list[asyncio.Future]:
        self.cnt_node = 0
        self.cnt_edges = 0
        return [*await self.nodes_bfs.execute(start), *await self.edges_bfs.execute(start)]

    def node(self, uuid: bytes) -> int:
        return self.__hom_node_dim[uuid]

    def dim(self, dim: int) -> bytes:
        return self.__hom_dim_node[dim]

    def edge(self, uuid: bytes) -> int:
        return self.__hom_edge_depth[uuid]

    def depth(self, depth: int) -> bytes:
        return self.__hom_depth_edge[depth]



class TensorRepresentation(object):

    def __init__(self):
        self.weight_tensor = None

