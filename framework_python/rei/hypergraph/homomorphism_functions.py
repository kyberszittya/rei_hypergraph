import asyncio

from rei.foundations.graph_monad import GraphMonad
from rei.foundations.hierarchical_traversal_strategies import DepthLimitedBreadthVisitChildren, HierarchicalTraversal
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge


class IndexHomomorphismGraphTensor(GraphMonad):

    def __init__(self, ignore_root: bool = False, depth: int = 1):
        super().__init__()
        # Counts
        self._cnt_node = 0
        self._cnt_edges = 0
        # Homology dictionaries
        # Mappings (unique identifiers to indices)
        self.__hom_node_dim: dict[bytes, int] = {}
        self.__hom_edge_depth: dict[bytes, int] = {}
        #self.__hom_values: dict[bytes, int] = {}
        # Reverse mappings (index to unique identifiers)
        self.__hom_dim_node: dict[int, bytes] = {}
        self.__hom_depth_edge: dict[int, bytes] = {}
        #self.__hom
        # Depth of mapping
        self._depth = depth
        # Traversals
        self.edges_bfs: HierarchicalTraversal = DepthLimitedBreadthVisitChildren(
            self.add_edge_homology, lambda x: isinstance(x, HypergraphEdge), self._depth, ignore_root)
        self.nodes_bfs: HierarchicalTraversal = DepthLimitedBreadthVisitChildren(
            self.add_node_homology, lambda x: isinstance(x, HypergraphNode), self._depth, ignore_root)
        # Multithreaded lock

    def add_edge_homology(self, arg: HypergraphEdge):
        # Edges homology
        i_current_edge = self._cnt_edges
        # Increment edge count
        self._cnt_edges += 1
        # Update indices
        self.__hom_edge_depth[arg.uuid] = i_current_edge
        self.__hom_depth_edge[i_current_edge] = arg.uuid

    def add_node_homology(self, arg: HypergraphNode):
        # Node homology
        i_current_node = self._cnt_node
        # Increment node count
        self._cnt_node += 1
        # Update indices
        self.__hom_node_dim[arg.uuid] = i_current_node
        self.__hom_dim_node[i_current_node] = arg.uuid

    async def execute(self, start) -> list[asyncio.Future]:
        self._cnt_node = 0
        self._cnt_edges = 0
        return [*await self.nodes_bfs.execute(start), *await self.edges_bfs.execute(start)]

    def node(self, uuid: bytes) -> int:
        return self.__hom_node_dim[uuid]

    def dim(self, dim: int) -> bytes:
        return self.__hom_dim_node[dim]

    def edge(self, uuid: bytes) -> int:
        return self.__hom_edge_depth[uuid]

    def depth(self, depth: int) -> bytes:
        return self.__hom_depth_edge[depth]

    @property
    def cnt_node(self):
        return self._cnt_node

    @property
    def cnt_edges(self):
        return self._cnt_edges
