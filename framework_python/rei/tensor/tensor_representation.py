import abc
import asyncio

import numpy as np
import copy

from rei.foundations.graph_monad import GraphMonad
from rei.hypergraph.base_elements import HypergraphNode, HypergraphRelation, HypergraphEdge
from rei.hypergraph.homomorphism_functions import IndexHomomorphismGraphTensor


class AbstractTensorRepresentation(metaclass=abc.ABCMeta):

    def __init__(self):
        self._weight_tensor = None
        self._incidence_matrix_out = None
        self._incidence_matrix_in = None
        self._current_homomorphism: IndexHomomorphismGraphTensor | None = None

    @property
    def W(self):
        return self._weight_tensor

    @property
    def Io(self):
        return self._incidence_matrix_out

    @property
    def Ii(self):
        return self._incidence_matrix_in

    @abc.abstractmethod
    def synchronize_structure_dimensions(self, homomorphism: IndexHomomorphismGraphTensor):
        raise NotImplementedError


class NumpyTensorRepresentation(AbstractTensorRepresentation):

    def synchronize_structure_dimensions(self, homomorphism: IndexHomomorphismGraphTensor):
        if self._current_homomorphism is not None:
            current_cnt_nodes, current_cnt_edges = self._current_homomorphism.cnt_node, self._current_homomorphism.cnt_edges
            del self._current_homomorphism
        else:
            current_cnt_nodes, current_cnt_edges = 0, 0
        self._current_homomorphism = copy.deepcopy(homomorphism)
        # If cnt nodes or cnt edges differs, reclaim weight tensor
        if homomorphism.cnt_node != current_cnt_nodes or homomorphism.cnt_edges != current_cnt_edges:
            # Weight tensor
            if self._weight_tensor is not None:
                del self._weight_tensor
            if self._incidence_matrix_out is not None:
                del self._incidence_matrix_out
            if self._incidence_matrix_in is not None:
                del self._incidence_matrix_in
            ho = self._current_homomorphism
            self._weight_tensor = np.zeros(shape=(ho.cnt_edges, ho.cnt_node, ho.cnt_node), dtype=np.float)
            self._incidence_matrix_out = np.zeros(shape=(ho.cnt_edges, ho.cnt_node), dtype=np.float)
            self._incidence_matrix_in = np.zeros(shape=(ho.cnt_edges, ho.cnt_node), dtype=np.float)

    def fill_weights(self, node: HypergraphNode):
        ho = self._current_homomorphism
        for e in node.sub_edges:
            e: HypergraphEdge
            for rel in e.sub_relations:
                rel: HypergraphRelation
                i_n = ho.node(rel.endpoint.uuid)
                i_e = ho.edge(e.uuid)
                # Fill weight
                self._weight_tensor[i_e, i_n, i_n] = rel.weight
                # Fill incidence
                self._incidence_matrix_out[i_e, i_n] = rel.relation_incidence_value[0]
                self._incidence_matrix_in[i_e, i_n] = rel.relation_incidence_value[1]


class NumpyHypergraphTensorTransformer(GraphMonad):

    def __init__(self) -> None:
        super().__init__()
        self._tensor_representation: AbstractTensorRepresentation | None = None

    async def execute(self, start) -> list[asyncio.Future]:
        homomorphism = IndexHomomorphismGraphTensor(True)
        _task_list = await homomorphism.execute(start)
        self._tensor_representation = NumpyTensorRepresentation()
        self._tensor_representation.synchronize_structure_dimensions(homomorphism)
        self._tensor_representation.fill_weights(start)
        return _task_list

    @property
    def tensor_representation(self):
        return self._tensor_representation



