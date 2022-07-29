from enum import IntEnum

import numpy as np

from cognitive.format.basicelements.concepts.network.base_definitions import NetworkElement, NetworkNode, \
    NetworkRelation, EnumRelationDirection
from cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge, \
    HyperEdgeConnection
from cognitive.format.hypergraph.foundations.hypergraph_operators import retrieve_part_hypergraph_node
from physics.geometry.basic_geometry import PrimitiveGeometry, calc_explicit_primitive_inertia


class KinematicLink(HypergraphNode):

    def __init__(self, name: str, timestamp: int,
                 mass: float = 1.0,
                 pose: np.ndarray = None,
                 subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        # Link specific attributes
        self._mass = mass
        if pose is None:
            self._pose = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        else:
            if pose.shape == (3,):
                self._pose = np.array([pose, [0.0, 0.0, 0.0]])
            else:
                self._pose = pose
        self.inertia = np.array([1., 1., 1., 0., 0., 0.])

    @property
    def mass(self) -> float:
        return self._mass

    @property
    def pose(self):
        return self._pose

    def str_pose(self):
        return f"{self._pose[0][0]} {self._pose[0][1]} {self._pose[0][2]} " \
               f"{self._pose[1][0]} {self._pose[1][1]} {self._pose[1][2]}"

    def calc_explicit_primitive_inertia(self, geom: PrimitiveGeometry):
        self.inertia = calc_explicit_primitive_inertia(self._mass, geom)


class KinematicGraph(HypergraphNode):

    def __init__(self, name: str, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self.kinematic_graphs = {}
        self.root_link: [KinematicLink | None] = None

    def add_kinematic_graph(self, a: HypergraphNode, timestamp: int):
        self.kinematic_graphs[a.id_name] = a
        self.add_subset(a, timestamp)

    def set_root_link(self, a: KinematicLink):
        self.root_link = a


class WorldLink(KinematicLink):

    def __init__(self, name: str, timestamp: int, mass: float = 1.0, pose: np.ndarray = None,
                 subsets: dict[bytes, NetworkElement] = None, parent: NetworkNode = None,
                 identitygen: InterfaceIdentifierGenerator = None, domain: MetaRegistry = None):
        super().__init__(name, timestamp, mass, pose, subsets, parent, identitygen, domain)


class KinematicJointType(IntEnum):
    FIXED = 0
    REVOLUTE = 1
    PRISMATIC = 2


class KinematicJoint(HypergraphEdge):

    def __init__(self, name: str, timestamp: int, parent: HypergraphNode,
                 identitygen: InterfaceIdentifierGenerator = None):
        super().__init__(name, timestamp, parent, identitygen)


def default_joint_axis():
    return np.array([0.0, 0.0, 1.0])


class KinematicJointConnection(HyperEdgeConnection):

    def __init__(self, name: str, timestamp: int,
                 joint_type: KinematicJointType = KinematicJointType.FIXED,
                 rigid_transformation: np.ndarray = None,
                 axis: np.ndarray = None,
                 domain: MetaRegistry = None, parent: NetworkRelation = None,
                 endpoint: HypergraphNode = None, value=None, identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, domain, parent, endpoint, value, identitygen, direction)
        self.joint_type: KinematicJointType = joint_type
        self._rigid_transformation: np.ndarray = rigid_transformation
        self._axis: np.ndarray = axis

    @property
    def rigid_transformation(self):
        if self._rigid_transformation is not None:
            return self._rigid_transformation
        else:
            return np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

    @property
    def axis(self):
        if self._axis is not None:
            return self._axis
        else:
            return default_joint_axis()


def connect_joint_to_node(context: HypergraphNode,
                          timestamp: int,
                          joint: KinematicJoint,
                          joint_type: KinematicJointType,
                          rigid_transformation: np.ndarray,
                          axis: np.ndarray,
                          target_qualified_name: str,
                          direction: EnumRelationDirection):
    joint.joint_type = joint_type
    target_name: str = '/'.join([context.progenitor_registry.qualified_name, target_qualified_name])
    res_target = list(retrieve_part_hypergraph_node(context, target_name))
    if len(res_target) != 0:
        target_node = res_target[0]
        joint.connect(res_target[0], 1, 0, direction)
        conn = KinematicJointConnection('/'.join([joint.id_name, target_node.id_name]), timestamp,
                                        joint_type, rigid_transformation, axis, joint.domain)
        joint.add_connection(conn, 0, target_node, direction)



def get_joint_type_from_antlr_relation(rel):
    match rel.joint_type().value_.text:
        case 'fix':
            return KinematicJointType.FIXED
        case 'rev':
            return KinematicJointType.REVOLUTE
        case 'tr':
            return KinematicJointType.PRISMATIC
    return KinematicJointType.FIXED


class GeometryNode(HypergraphNode):

    def __init__(self, name: str, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)


class CollisionGeometry(GeometryNode):

    def __init__(self, name: str, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)


class VisionGeometry(GeometryNode):

    def __init__(self, name: str, timestamp: int,
                 material_name: str = None,
                 subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self.material_name = material_name


class KinematicJointRelation(HyperEdgeConnection):

    def __init__(self, name: str, timestamp: int, domain: MetaRegistry, parent: NetworkRelation,
                 endpoint: HypergraphNode, value=None, identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, domain, parent, endpoint, value, identitygen, direction)


class FixKinematicJointRelation(KinematicJointRelation):

    def __init__(self, name: str, timestamp: int, domain: MetaRegistry, parent: NetworkRelation,
                 endpoint: HypergraphNode, value=None, identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, domain, parent, endpoint, value, identitygen, direction)
