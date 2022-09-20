import typing

from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import MetaClock
from rei.fuzzy.fuzzy_engine import FuzzyEngine
from rei.fuzzy.fuzzy_nodes import FuzzifierNode, FuzzyLinguisticNode, FuzzyRuleNode, FuzzyRuleTerminalNode, \
    FuzzyComputationEdge
from rei.fuzzy.norm_functions import MaxNorm, MinNorm, SNorm
from rei.hypergraph.base_elements import HypergraphNode
from rei.hypergraph.common_definitions import EnumRelationDirection


class FuzzyElementFactory(HypergraphFactory):

    def __init__(self, factory_name: str, clock: MetaClock) -> None:
        super().__init__(factory_name, clock)

    def create_fuzzy_engine(self, id_name: str, parent: HypergraphNode = None) -> FuzzyEngine:
        if parent is not None:
            uid = self.unique_identifier.generate_uid('/'.join([parent.qualified_name, id_name]))
        else:
            uid = self.unique_identifier.generate_uid(id_name)
        node = FuzzyEngine(id_name, uid, '/'.join([self._factory_name, self.get_qualified_name(id_name)]),
                           self._clock, parent)
        return node

    def create_fuzzy_computation_node(self, id_name: str,
                                      values: list,
                                      parent: HypergraphNode = None):
        __node = self.generate_node(id_name, parent)
        __values = self.create_value(__node, "values", values)
        return __node, __values

    def create_computation_edge(
            self, id_name: str, parent: HypergraphNode, fuzzy_inputs: list[FuzzifierNode],
            fuzzy_outputs: list[FuzzifierNode], fuzzy_ling_name: list):
        connections: list = []
        for v in fuzzy_inputs:
            connections.append((v, EnumRelationDirection.INWARDS, None, None))
        for v in fuzzy_outputs:
            connections.append((v, EnumRelationDirection.OUTWARDS, None, None))
        for v in fuzzy_ling_name:
            connections.append((v, EnumRelationDirection.INWARDS, None, None))
        __fhe: FuzzyComputationEdge = self.__create_fuzzy_computational_edge(id_name, parent)
        self.connect_tuple_nodes(parent, id_name, connections, __fhe)
        # Create value node for generated values
        self.create_value(__fhe, "input_value_labels", [x.id_name for x in fuzzy_ling_name])
        return __fhe

    def __create_fuzzy_computational_edge(self, edge_name, container):
        uuid: bytes = self.unique_identifier.generate_uid(edge_name)
        qname = self.get_stamped_qualified_name(edge_name, container)
        return FuzzyComputationEdge(edge_name, uuid, qname, container.clock, container)

    def __generate_fuzzifier_node(self, id_name: str, parent: HypergraphNode = None) -> FuzzifierNode:
        uid = self._generate_node_uid(id_name, parent)
        qname = self._generate_node_qualified_name(id_name)
        return FuzzifierNode(id_name, uid, qname, self._clock, parent)

    def create_fuzzifier_node(self, id_name: str, parent: HypergraphNode,
                       membership: list[typing.Callable],
                       hyperparameters: list[list[float]]) -> FuzzifierNode:
        __fuzzifier_node = self.__generate_fuzzifier_node(id_name, parent)
        self.create_value(__fuzzifier_node, "membership", membership)
        self.create_value(__fuzzifier_node, "hyperparameters", hyperparameters)
        self.create_value(__fuzzifier_node, "values", [])
        return __fuzzifier_node

    def __create_rule_node(self, id_name: str, parent: HypergraphNode):
        uid = self._generate_node_uid(id_name, parent)
        qname = self._generate_node_qualified_name(id_name)
        return FuzzyRuleNode(id_name, uid, qname, self._clock, parent)

    def create_rule(self, rule_name: str, parent, fuzzy_variables: list[FuzzifierNode], precedent, antecedent):
        __rule = self.__create_rule_node(rule_name, parent)
        value_label_mappings = {}
        value_node_mappings = {}
        for v in fuzzy_variables:
            v: FuzzifierNode
            value_label_mappings[v.labels.id_name] = v.labels
            value_node_mappings[v.labels.id_name] = v
        __tnorm = self.__generate_t_norm(".".join([rule_name, "tnorm"]), __rule)
        __snorm = self.__generate_s_norm(".".join([rule_name, "snorm"]), __rule)
        for p in precedent:
            indices = [value_label_mappings[p[0]].homology_label_to_index[v] for v in p[1]]
            self.__create_rule_terminal_node(__tnorm, '.'.join(['rule', p[0]]), value_node_mappings[p[0]],
                                             indices, __snorm)
        for a in antecedent:
            indices = [value_label_mappings[a[0]].homology_label_to_index[v] for v in a[1]]
            self.__create_rule_terminal_node(__rule, '.'.join(['rule_result', a[0]]), value_node_mappings[a[0]],
                                             indices, __snorm)
        return __rule

    def __generate_linguistic_node(self, id_name: str, parent: HypergraphNode):
        uid = self._generate_node_uid(id_name, parent)
        qname = self._generate_node_qualified_name(id_name)
        return FuzzyLinguisticNode(id_name, uid, qname, self._clock, parent)

    def __generate_s_norm(self, id_name: str, parent: HypergraphNode):
        uid = self._generate_node_uid(id_name, parent)
        qname = self._generate_node_qualified_name(id_name)
        return MaxNorm(id_name, uid, qname, self._clock, parent)

    def __generate_t_norm(self, id_name: str, parent: HypergraphNode):
        uid = self._generate_node_uid(id_name, parent)
        qname = self._generate_node_qualified_name(id_name)
        return MinNorm(id_name, uid, qname, self._clock, parent)

    def create_linguistic_node(self, id_name: str, parent: HypergraphNode, labels: typing.Iterable[str]):
        __linguistic_node = self.__generate_linguistic_node(id_name, parent)
        self.create_value(__linguistic_node, "labels", labels)
        __linguistic_node.update()
        return __linguistic_node

    def connect_fuzzifier_node(self, parent: HypergraphNode, ling: FuzzyLinguisticNode,
                               fuzzifiernode: HypergraphNode, direction: EnumRelationDirection,
                               valuenode: HypergraphNode, input_value_labels: list[str], bounds: list[float]):
        id_name = '_'.join(["fuzz", valuenode.id_name, fuzzifiernode.id_name, *input_value_labels])
        match direction:
            case EnumRelationDirection.INWARDS:
                __he = self.connect_tuple_nodes(parent, id_name,
                                                [(valuenode, EnumRelationDirection.INWARDS, None, None),
                                                 (ling, EnumRelationDirection.INWARDS, None, None),
                                                 (fuzzifiernode, EnumRelationDirection.OUTWARDS, None, None)])
            case EnumRelationDirection.OUTWARDS:
                __he = self.connect_tuple_nodes(parent, id_name,
                                                [(valuenode, EnumRelationDirection.OUTWARDS, None, None),
                                                 (ling, EnumRelationDirection.INWARDS, None, None),
                                                 (fuzzifiernode, EnumRelationDirection.INWARDS, None, None)])
            case _:
                raise RuntimeError
        self.create_value(__he, "input_value_labels", input_value_labels)
        self.create_value(__he, "bounds", bounds)
        fuzzifiernode.update()
        return __he

    def __create_rule_terminal_node(self, parent: HypergraphNode, id_name: str, variable: FuzzifierNode,
                                    proj_index: list[int], norm: SNorm):
        uid = self._generate_node_uid(id_name, parent)
        qname = self._generate_node_qualified_name(id_name)
        return FuzzyRuleTerminalNode(id_name, uid, qname, self._clock, norm, proj_index, variable, parent)

