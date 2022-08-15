import asyncio

from rei.foundations.graph_monad import GraphMonad
from rei.foundations.hierarchical_traversal_strategies import DepthLimitedBreadthVisitChildren, HierarchicalTraversal
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge
from rei.hypergraph.value_node import ValueNode


class IndexHomomorphismGraphTensor(GraphMonad):

    def __init__(self, ignore_root: bool = False, depth: int = 1):
        super().__init__()
        # Counts
        self._ignore_root = True
        #
        self._cnt_node = 0
        self._cnt_edges = 0
        self._cnt_values = 0
        # Homology dictionaries
        # Mappings (unique identifiers to indices)
        self.__hom_node_dim: dict[bytes, int] = {}
        self.__hom_edge_depth: dict[bytes, int] = {}
        self.__hom_values: dict[bytes, int] = {}
        # Reverse mappings (index to unique identifiers)
        self.__hom_dim_node: dict[int, bytes] = {}
        self.__hom_depth_edge: dict[int, bytes] = {}
        self.__hom_i_values: dict[int, bytes] = {}
        # Depth of mapping
        self._depth = depth
        # Traversals
        self.edges_bfs: HierarchicalTraversal = DepthLimitedBreadthVisitChildren(
            self.add_edge_homology, lambda x: isinstance(x, HypergraphEdge), self._depth, ignore_root)
        self.nodes_bfs: HierarchicalTraversal = DepthLimitedBreadthVisitChildren(
            self.add_node_homology, lambda x: isinstance(x, HypergraphNode), self._depth, ignore_root)
        self.values_bfs: HierarchicalTraversal = DepthLimitedBreadthVisitChildren(
            self.add_value_homology, lambda x: isinstance(x, ValueNode), self._depth, ignore_root
        )

    def reset_from_bijection(self, nodes, edges, values):
        self.reset_homology()
        # Node homology
        for n, i in nodes:
            self.__hom_node_dim[n] = i
            self.__hom_dim_node[i] = n
            self._cnt_node += 1
        # Edge homology
        for e, i in edges:
            self.__hom_edge_depth[e] = i
            self.__hom_depth_edge[i] = e
            self._cnt_edges += 1
        # Value homology
        for v, i in values:
            self.__hom_values[v] = i
            self.__hom_i_values[i] = v
            self._cnt_values += 1

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

    def add_value_homology(self, arg: ValueNode):
        # Value homology
        i_current_value = self._cnt_values
        # Increment value count
        self._cnt_values += 1
        # Update indices
        self.__hom_values[arg.uuid] = i_current_value
        self.__hom_i_values[i_current_value] = arg.uuid

    def reset_homology(self):
        self._cnt_node = 0
        self._cnt_edges = 0
        self._cnt_values = 0
        # Homology dictionaries
        # Mappings (unique identifiers to indices)
        self.__hom_node_dim: dict[bytes, int] = {}
        self.__hom_edge_depth: dict[bytes, int] = {}
        self.__hom_values: dict[bytes, int] = {}
        # Reverse mappings (index to unique identifiers)
        self.__hom_dim_node: dict[int, bytes] = {}
        self.__hom_depth_edge: dict[int, bytes] = {}
        self.__hom_i_values: dict[int, bytes] = {}

    async def execute(self, start) -> list[asyncio.Future]:
        self.reset_homology()
        return [*await self.nodes_bfs.execute(start), *await self.edges_bfs.execute(start)]

    def node(self, uuid: bytes) -> int:
        return self.__hom_node_dim[uuid]

    def dim(self, dim: int) -> bytes:
        return self.__hom_dim_node[dim]

    def edge(self, uuid: bytes) -> int:
        return self.__hom_edge_depth[uuid]

    def depth(self, depth: int) -> bytes:
        return self.__hom_depth_edge[depth]

    def val(self, uuid: bytes) -> int:
        return self.__hom_values[uuid]

    def ival(self, i: int) -> bytes:
        return self.__hom_i_values[i]

    @property
    def cnt_node(self):
        return self._cnt_node

    @property
    def cnt_edges(self):
        return self._cnt_edges
