import typing

from rei.factories.abstract_factory import AbstractElementFactory, ErrorInsufficientValues
from rei.foundations.clock import MetaClock
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge, HypergraphElement
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.value_node import ValueNode, SemanticValueNode


class HypergraphFactory(AbstractElementFactory):

    def __init__(self, factory_name: str, clock: MetaClock) -> None:
        super().__init__(factory_name, clock)

    def _generate_node_uid(self, id_name: str, parent: HypergraphNode) -> bytes:
        if parent is not None:
            return self.unique_identifier.generate_uid('/'.join([parent.qualified_name, id_name]))
        return self.unique_identifier.generate_uid(id_name)

    def _generate_node_qualified_name(self, id_name: str):
        return '/'.join([self._factory_name, self.get_qualified_name(id_name)])

    def generate_node(self, id_name: str, parent: HypergraphNode = None) -> HypergraphNode:
        uid = self._generate_node_uid(id_name, parent)
        qname = self._generate_node_qualified_name(id_name)
        node = HypergraphNode(id_name, uid, qname, self._clock, parent)
        return node

    def generate_list_nodes(self, id_name: list[str], parent: HypergraphNode = None) -> list[HypergraphNode]:
        return [self.generate_node(name, parent) for name in id_name]

    #
    # Generator functions
    #

    def create_hyperedge(self, parent: HypergraphNode, edge_name: str):
        uuid: bytes = self.unique_identifier.generate_uid(edge_name)
        he = HypergraphEdge(edge_name, uuid,
                            self.get_stamped_qualified_name(edge_name, parent),
                            parent.clock, parent)
        return he

    def connect_nodes(self, container: HypergraphNode, edge_name: str, nodes: list[HypergraphNode],
                      direction: EnumRelationDirection = EnumRelationDirection.BIDIRECTIONAL,
                      values: list[ValueNode] | None = None):
        uuid: bytes = self.unique_identifier.generate_uid(edge_name)
        he = HypergraphEdge(edge_name, uuid, self.get_stamped_qualified_name(edge_name, container), container.clock, container)
        if values is None:
            node_values = zip(nodes, len(nodes)*[None])
        else:
            if len(values) != len(nodes):
                raise ErrorInsufficientValues
            node_values = zip(nodes, values)
        for n,v in node_values:
            he.unary_connect(n, v, direction)
        return he

    def connect_2factor_edges(
            self, container: HypergraphNode, edge_name: str, in_dir_nodes: list[HypergraphNode],
            out_dir_nodes: list[HypergraphNode], direction: tuple[EnumRelationDirection, EnumRelationDirection],
            values: list[ValueNode] | None = None):
        uuid: bytes = self.unique_identifier.generate_uid(edge_name)
        he = HypergraphEdge(edge_name, uuid, self.get_stamped_qualified_name(edge_name, container), container.clock, container)
        if values is None:
            node_in_values = zip(in_dir_nodes, (len(in_dir_nodes))*[None])
            node_out_values = zip(out_dir_nodes, (len(out_dir_nodes))*[None])
        else:
            if len(values) != (len(out_dir_nodes)+len(in_dir_nodes)):
                raise ErrorInsufficientValues
            node_in_values = zip(in_dir_nodes, values[:len(in_dir_nodes)])
            node_out_values = zip(out_dir_nodes, values[len(in_dir_nodes):])
        for n,v in node_in_values:
            he.unary_connect(n, v, direction[0])
        for n,v in node_out_values:
            he.unary_connect(n, v, direction[0])
        return he

    def connect_dir_edges(self, container: HypergraphNode, edge_name: str, in_dir_nodes: list[HypergraphNode],
                          out_dir_nodes: list[HypergraphNode]):
        return self.connect_2factor_edges(container, edge_name, in_dir_nodes, out_dir_nodes,
                                          (EnumRelationDirection.INWARDS, EnumRelationDirection.OUTWARDS))

    def _create_edge(self, edge_name: str, container: HypergraphNode):
        uuid: bytes = self.unique_identifier.generate_uid(edge_name)
        qname = self.get_stamped_qualified_name(edge_name, container)
        return HypergraphEdge(edge_name, uuid, qname, container.clock, container)

    def connect_tuple_nodes(
            self, container: HypergraphNode, edge_name: str,
            nodes: list[tuple[HypergraphNode, EnumRelationDirection, ValueNode | None | dict, SemanticValueNode | None]],
            edge: HypergraphEdge = None):
        """

        :param container:
        :param edge_name:
        :param nodes: endpoint, direction, value node, semantiv calue node
        :return:
        """
        if edge is None:
            he = self._create_edge(edge_name, container)
        else:
            he = edge
        # Connect elements
        for n, dir, v, sv in nodes:
            he.unary_connect(n, v, dir, sv)
        return he

    def create_value(self, parent: HypergraphElement | None, value_name: str, values: list[typing.Any] = None):
        uuid: bytes = self.unique_identifier.generate_uid(value_name)
        if parent is not None:
            val = ValueNode(uuid, value_name, self.get_stamped_qualified_name(value_name, parent), values)
            parent.add_element(val)
        else:
            val = ValueNode(uuid, value_name, '/'.join([value_name])+f".{self._clock.get_time_ns()}", values)
        return val
