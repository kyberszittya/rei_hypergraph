import abc
import asyncio
import queue

import numpy as np
import copy


from rei.foundations.graph_monad import GraphMonad
from rei.foundations.hypergraph_traversal_strategies import HypergraphTraversal
from rei.hypergraph.homomorphism_functions import IndexHomomorphismGraphTensor
from rei.hypergraph.norm.norm_functions import SumNorm


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

    @property
    def deg(self):
        return self.degree_matrix()

    @property
    def D(self):
        return self.diag_degree_matrix()

    @property
    def L(self):
        return self.calc_laplacian()

    @property
    def Lp(self):
        return self.calc_projected_laplacian()

    @property
    def DD(self):
        return self.diag_degree_tensor()

    @property
    def Lnorm(self):
        return self.calc_normalized_laplacian()

    @property
    def total_deg(self):
        return self.calc_total_deg()

    @abc.abstractmethod
    def calc_total_deg(self):
        raise NotImplementedError

    @abc.abstractmethod
    def degree_matrix(self):
        raise NotImplementedError

    @abc.abstractmethod
    def diag_degree_matrix(self):
        raise NotImplementedError

    @abc.abstractmethod
    def diag_degree_tensor(self):
        raise NotImplementedError

    @abc.abstractmethod
    def calc_laplacian(self):
        raise NotImplementedError

    @abc.abstractmethod
    def calc_projected_laplacian(self):
        raise NotImplementedError

    @abc.abstractmethod
    def synchronize_structure_dimensions(self, homomorphism: IndexHomomorphismGraphTensor):
        raise NotImplementedError

    @abc.abstractmethod
    def calc_normalized_laplacian(self):
        raise NotImplementedError

    @abc.abstractmethod
    def entropy(self):
        raise NotImplementedError


class NumpyTensorRepresentation(AbstractTensorRepresentation):




    def degree_matrix(self):
        coeff = 1.0/(np.all(self.Io == self.Ii, axis=0) + 1)
        return np.multiply(np.sum(self.Io, axis=0) + np.sum(self.Ii, axis=0), coeff)

    def diag_degree_matrix(self):
        return np.diag(self.degree_matrix())

    def calc_total_deg(self):
        return np.sum(self.degree_matrix())

    def calc_laplacian(self):
        return self.DD - self.W

    def calc_projected_laplacian(self):
        return self.D - np.sum(self.W, axis=0)

    def diag_degree_tensor(self):
        coeff = np.apply_along_axis(np.diag, 1,
                                    1.0/((np.sum(self.W, axis=1) == np.sum(self.W, axis=2)).astype(float) + 1))
        __DD = np.apply_along_axis(np.diag, 1, np.sum(self.W, axis=1))
        return __DD @ coeff

    def calc_normalized_laplacian(self):
        # As per Ouvrard
        return 1.0/(self.Ii.shape[0] - 1) * self.L/np.sqrt(self.deg)

    def entropy(self):
        di = self.calc_normalized_laplacian().diagonal(axis1=1, axis2=2)
        return -di*np.nan_to_num(np.log2(di), neginf=0, posinf=0)

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

    def fill_tensors(self, i_e, i_n0, i_n1, i_w, val):
        self._weight_tensor[i_e, i_n1, i_n0] = i_w
        # Fill incidence
        self._incidence_matrix_out[i_e, i_n1] = i_w
        self._incidence_matrix_in[i_e, i_n0] = i_w

    async def fill_weights(self, q, _task_list: list):
        while not q.empty():
            for v in q.get():
                i_n0, i_n1, i_e, i_w, val = v
                # Fill weight
                self.fill_tensors(i_e, i_n1, i_n0, i_w, val)


class NumpyHypergraphTensorTransformer(GraphMonad):

    def __init__(self, repr_depth: int = 1) -> None:
        super().__init__()
        self._tensor_representation: AbstractTensorRepresentation | None = None
        self.repr_depth = repr_depth

    async def execute(self, start) -> list[asyncio.Future]:
        homomorphism = IndexHomomorphismGraphTensor(True)
        _task_list = await homomorphism.execute(start)
        self._tensor_representation = NumpyTensorRepresentation()
        self._tensor_representation.synchronize_structure_dimensions(homomorphism)
        q = queue.Queue()
        tr = HypergraphTraversal(lambda x: q.put(x), lambda x: True, SumNorm(), homomorphism, self.repr_depth)
        await tr.execute(start)
        await self._tensor_representation.fill_weights(q, _task_list)
        return _task_list

    @property
    def tensor_representation(self):
        return self._tensor_representation
