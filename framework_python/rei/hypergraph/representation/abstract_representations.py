import abc

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
    def entropy_vector(self):
        raise NotImplementedError

    @abc.abstractmethod
    def entropy(self):
        raise NotImplementedError

    @abc.abstractmethod
    def entropy_projected(self):
        raise NotImplementedError


