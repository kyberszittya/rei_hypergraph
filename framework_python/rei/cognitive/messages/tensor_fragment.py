import numpy as np

from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from rei.cognitive.messages.message_fragment import FragmentMessage


class FragmentTensor(FragmentMessage):



    # TODO: complete fragment
    def __init__(self, tensor_values: np.array, hierarchy_array: np.array, incidence_array: np.array, edge_hierarchy: np.array,
                 id_name: str = "", timestamp: int = 0, identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(id_name, timestamp, identitygen)
        # Tensor values
        self._tensor_values = tensor_values
        self._hierarchy_array = hierarchy_array
        self._incidence_array = incidence_array
        self._edge_hierarchy_array = edge_hierarchy

    def register(self, registry, timestamp: int) -> None:
        pass

    def deregister(self):
        pass

    def reregister(self, new_registy, timestamp: int):
        pass

    @property
    def tensor_values(self):
        return self._tensor_values

    @property
    def V(self):
        return self._tensor_values

    @property
    def hierarchy_array(self):
        return self._hierarchy_array

    @property
    def Hi(self):
        return self._hierarchy_array

    @property
    def adjacency_array(self):
        return self._incidence_array

    @property
    def I(self):
        return self._incidence_array

    @property
    def edge_hiearchy_array(self):
        return self._edge_hierarchy_array

    @property
    def EH(self):
        return self._edge_hierarchy_array

    def serialize_bytes(self) -> bytes:
        pass

    def degree_matrix_outwards(self):
        d_out = np.sum(self.V.T, axis=2)
        return np.apply_along_axis(np.diag, 1, d_out)

    def degree_matrix_inwards(self):
        d_in = np.sum(self.V.T, axis=1)
        return np.apply_along_axis(np.diag, 1, d_in)

    def degree_matrix(self):
        return np.apply_along_axis(np.diag, 1, np.sum(self._tensor_values.T, 1))

    @property
    def D(self):
        return self.degree_matrix()

    def laplacian_matrix(self):
        return self.D - self._tensor_values.T

    @property
    def L(self):
        return self.laplacian_matrix()