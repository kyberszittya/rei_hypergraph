from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkElement, NetworkNode
from rei.cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode

import numpy as np


class PrimitiveGeometry(HypergraphNode):

    def __init__(self, name: str, timestamp: int,
                 dimensions: np.ndarray,
                 subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self.dimensions = dimensions


# Geometries

class PolyhedronGeometry(PrimitiveGeometry):

    def __init__(self, name: str, timestamp: int,
                 dimensions: np.ndarray,
                 subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, dimensions, subsets, parent, identitygen, domain)


class EllipsoidGeometry(PrimitiveGeometry):

    def __init__(self, name: str, timestamp: int,
                 dimensions: np.ndarray,
                 subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, dimensions, subsets, parent, identitygen, domain)


class CylinderGeometry(PrimitiveGeometry):

    def __init__(self, name: str, timestamp: int,
                 dimensions: np.ndarray,
                 subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, dimensions, subsets, parent, identitygen, domain)


class MeshGeometry(PrimitiveGeometry):

    def __init__(self, name: str, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)


def calc_explicit_primitive_inertia(mass: float, geom: PrimitiveGeometry):
    inertia_vector = np.zeros(6)
    match geom:
        case PolyhedronGeometry():
            if geom.dimensions.shape == (3,):
                # Check whether a cuboid
                c = 1.0/12.0*mass
                inertia_vector[0] = c*(geom.dimensions[1]**2 + geom.dimensions[2]**2)
                inertia_vector[1] = c*(geom.dimensions[0]**2 + geom.dimensions[2]**2)
                inertia_vector[2] = c*(geom.dimensions[0]**2 + geom.dimensions[1]**2)
        case EllipsoidGeometry():
            if geom.dimensions.shape == (1,):
                # It's just a plain old sphere
                _I = 2.0/3.0 * mass * geom.dimensions[0]**2
                inertia_vector[0] = _I
                inertia_vector[1] = _I
                inertia_vector[2] = _I
        case CylinderGeometry():
            if geom.dimensions.shape == (2,):
                # Cylinder with no other dimension values whatsoever
                _I = 1.0/12.0*mass*(3.0 * geom.dimensions[0]**2 + geom.dimensions[1]**2)
                inertia_vector[0] = _I
                inertia_vector[1] = _I
                inertia_vector[2] = 0.5 * mass * geom.dimensions[0]**2
    return inertia_vector
