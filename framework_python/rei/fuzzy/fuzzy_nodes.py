import copy

import numpy as np

from rei.foundations.clock import MetaClock
from rei.foundations.conceptual_item import HierarchicalElement
from rei.fuzzy.norm_functions import SNorm, TNorm
from rei.hypergraph.base_elements import HypergraphNode, HypergraphRelation, HypergraphEdge
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.value_node import ValueNode


class FuzzyLinguisticNode(HypergraphNode):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None) -> None:
        super().__init__(id_name, uuid, qualified_name, clock, parent)
        # Labels
        self._labels = None
        # Homologies
        self._homology_label_to_index = {}

    def update(self):
        super().update()
        self._labels = next(self.get_values("labels"), None)
        if self._labels is not None:
            self._homology_label_to_index = {k:i for i,k in enumerate(self._labels.get_values())}

    @property
    def labels(self):
        return self._labels.get_values()

    @property
    def homology_label_to_index(self):
        return copy.copy(self._homology_label_to_index)


# Fuzzy computation node

class FuzzifierNode(HypergraphNode):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None) -> None:
        # Fuzzy attributes
        self._membership = None
        self._hyperparameters = None
        self._labels = None
        # Invoke super-constructor
        super().__init__(id_name, uuid, qualified_name, clock, parent)
        # Cache value elements
        self._value = {}
        self._norm_bounds = {}
        self._last_values = None
        # Label mapping homomorphism
        self._homology_label_to_index = {}

    def __obtain_labels(self):
        for p in self.sub_ports:
            for r in filter(lambda x: isinstance(x.endpoint, FuzzyLinguisticNode), p.endpoint.parent.get_incoming_relations()):
                yield r.endpoint
        yield None

    def update(self):
        super().update()
        self._membership = next(self.get_values("membership"), None)
        self._hyperparameters = next(self.get_values("hyperparameters"), None)
        # Search for lingusitic values
        _labels = next(self.__obtain_labels(), None)
        if _labels is not None:
            self._labels = _labels

    @property
    def labels(self) -> FuzzyLinguisticNode:
        return self._labels


    def __update_relations(self, __input_value_label: str, r: HypergraphRelation):
        __parent_edge: HypergraphEdge = r.endpoint.parent
        for rel in __parent_edge.get_incoming_relations():
            for v in list(rel.endpoint.get_values(__input_value_label)):
                self._value[__input_value_label] = v

    def fuzzify(self):
        res = None
        __label_vals = next(self._labels.get_values("labels")).get_values()
        for me, par, lab in zip(self._membership.get_values(), self._hyperparameters.get_values(), __label_vals):
            for r in filter(lambda x: x.endpoint.direction == EnumRelationDirection.OUTWARDS, self.sub_ports):
                _v = next(r.endpoint.parent.get_values("input_value_labels"))
                __input_value_label = _v.get_values()[0]
                # Get recent values
                if __input_value_label not in self._value:
                    self.__update_relations(__input_value_label, r)
                # Value
                _x = self._value[__input_value_label].get_values()
                # Bound setup
                __bound_val = next(r.endpoint.parent.get_values("bounds"), None)
                if __bound_val is not None:
                    __bound = __bound_val.get_values()
                    _x = 2.0 * (_x - __bound[0])/(__bound[1] - __bound[0]) - 1
                _x = me(_x, *par)
                if res is None:
                    res = _x
                else:
                    res = np.vstack((res, _x))
        # Update values
        self._last_values = res
        next(self.get_values("values")).update_values(res)

    @property
    def last_values(self):
        return self._last_values

# Fuzzy rule node


class FuzzyRuleNode(HypergraphNode):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None) -> None:
        super().__init__(id_name, uuid, qualified_name, clock, parent)

    def eval(self):
        res = None
        for s in self.get_subelements(lambda x: isinstance(x, TNorm)):
            _terms = s.get_subelements(lambda x: isinstance(x, FuzzyRuleTerminalNode))
            s_res = None
            for term in _terms:
                if len(term.proj_index) == 1:
                    s_res = term.last_values[term.proj_index]
                else:
                    term_res = term.eval()
                    if s_res is None:
                        s_res = term_res
                    else:
                        s_res = np.vstack(s_res, term_res)
            if res is None:
                res = s_res
            else:
                res = np.vstack(res, s_res)
        for s in self.get_subelements(lambda x: isinstance(x, FuzzyRuleTerminalNode)):
            s: FuzzyRuleTerminalNode
            __v = next(s.fuzzy_var.get_values("values"))
            v = __v.get_values()
            __label = s.fuzzy_var.labels.labels
            if isinstance(v, list) or len(v) == 0:
                __space = np.zeros((len(__label), res.shape[1]))
            else:
                __space = v
            __space[s.proj_index] = res
            __v.update_values(__space)
        return __space


class FuzzyRuleTerminalNode(HypergraphNode):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock, snorm: SNorm,
                 proj_index: list[int], variable: FuzzifierNode, parent: HierarchicalElement = None) -> None:
        super().__init__(id_name, uuid, qualified_name, clock, parent)
        self._proj_index = proj_index
        self._snorm = snorm
        self._fuzzy_var = variable

    @property
    def proj_index(self):
        return self._proj_index
    
    @property
    def last_values(self):
        return self._fuzzy_var.last_values

    @property
    def fuzzy_var(self):
        return self._fuzzy_var

    def eval(self):
        _x = self._snorm.eval(self.last_values[self.proj_index])
        return _x


# Fuzzy edge


class FuzzyComputationEdge(HypergraphEdge):

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None):
        super().__init__(id_name, uuid, qualified_name, clock, parent)
        self._snorm = None
        self._tnorm = None

    def update(self):
        super().update()
        self._snorm = next(self.get_values("snorm"), None)
        self._tnorm = next(self.get_values("tnorm"), None)

    def eval(self):
        res = None
        # Exceute TNORM
        for s in self.get_subelements(lambda x: isinstance(x, FuzzyRuleNode)):
            if res is None:
                res = s.eval()
            else:
                # TODO: revise this part
                res = np.max(np.stack((s.eval(), res), axis=2), axis=2)
        # Update values
        for r in filter(lambda x: isinstance(x.endpoint, FuzzyLinguisticNode), self.get_incoming_relations()):
            r: HypergraphRelation
            for v in r.endpoint.get_values(r.endpoint.id_name):
                v: ValueNode
                v.update_values(np.max(res, axis=0))
            for v in r.endpoint.get_values("raw_"+r.endpoint.id_name):
                v: ValueNode
                v.update_values(res)
        return res
