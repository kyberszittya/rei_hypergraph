import numpy as np

from rei.format.phys.solid_geometry_context import encode_geometry_element
from rei.format.semantics.CognitiveEntity import RigidTransformation, KinematicLink, KinematicJoint, InertiaElement, \
    KinematicGraphDefinition
from lxml import etree

from rei.hypergraph.base_elements import HypergraphPort, HypergraphNode, HypergraphEdge, HypergraphRelation
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.query.query_engine import HierarchicalPrepositionQuery
from test.common.common_util import join_w_separator, join_w_prefix_separator

__DEFAULT_RIGID_TRANSFORMATION = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
__REI_KINEMATIC_ELEMENT_SEPARATOR = '.'

def extract_rigid_transformation_element(x: RigidTransformation):
    el_pose = etree.Element("pose")
    rot = [x for x in x['rotation']]
    match x['rotation_type']:
        case 'deg':
            rot = [np.pi/180.0*x for x in rot]
    el_pose.text = f"{x['translation'][0]} {x['translation'][1]} {x['translation'][2]} {rot[0]} {rot[1]} {rot[2]}"
    # Set relative frame
    return el_pose


def __default_rigid_transformation_element():
    el_pose = etree.Element("pose")
    el_pose.text = ' '.join([str(x) for x in __DEFAULT_RIGID_TRANSFORMATION])
    # Set relative frame
    return el_pose

def get_parent_kinematic_graph(node: HypergraphNode):
    # Check if node
    __current_node = node
    while True:
        l = list(__current_node.get_subelements(lambda x: isinstance(x, KinematicGraphDefinition)))
        if len(l) > 0:
            return (l[0], __current_node)
        if __current_node.parent is not None:
            __current_node = __current_node.parent
        else:
            break
    return None, None


def __obtain_relative_frame_name(node: HypergraphNode):
    kin_graph, parent_kin_graph = get_parent_kinematic_graph(node)
    #print(parent_kin_graph.id_name)
    # Check relative frame
    relative_frame_name = None
    for x in node.sub_ports:
        # Normal
        x: HypergraphPort
        __rel: HypergraphRelation = x.endpoint
        sub_el = next(__rel.get_subelements(lambda y: isinstance(y, KinematicJoint)))
        if sub_el is not None:
            if __rel.direction == EnumRelationDirection.OUTWARDS:
                e: HypergraphEdge = x.endpoint.parent
                incom = list(filter(lambda _r: _r.endpoint.id_name != "world", e.get_incoming_relations()))
                if len(incom) > 0:
                    relative_frame_name = sub_el.id_name
                    return relative_frame_name
            else:
                # We are instantiating a reference
                _, con_kin_graph = get_parent_kinematic_graph(parent_kin_graph.parent)
                if con_kin_graph is not None:
                    relative_frame_name = '.'.join(["connect", node.id_name])
    return relative_frame_name


def encode_link_element(element: KinematicLink, prefix=""):
    link_el = etree.Element("link")
    link_el.attrib["name"] = join_w_prefix_separator([element.id_name], __REI_KINEMATIC_ELEMENT_SEPARATOR, prefix)
    #
    cont_node: HypergraphNode = element.parent
    relative_frame_name = __obtain_relative_frame_name(cont_node)
    # Inertia
    # TODO: finish it
    for x in element.get_subelements(lambda x: isinstance(x, InertiaElement)):
        print("inert")
    # Rigid transformation
    for x in element.get_subelements(lambda x: isinstance(x, RigidTransformation)):
        el_joint_pose = extract_rigid_transformation_element(x)
        # Check relative frame
        if relative_frame_name is not None:
            el_joint_pose.attrib["relative_to"] = join_w_prefix_separator(
                [relative_frame_name], __REI_KINEMATIC_ELEMENT_SEPARATOR, prefix)
        # Add pose to joint
        link_el.append(el_joint_pose)
        break
    else:
        el_joint_pose = __default_rigid_transformation_element()
        # Check relative frame
        if relative_frame_name is not None:
            el_joint_pose.attrib["relative_to"] = join_w_prefix_separator(
                [relative_frame_name], __REI_KINEMATIC_ELEMENT_SEPARATOR, prefix)
        link_el.append(el_joint_pose)
    for el in encode_geometry_element(cont_node, prefix):
        link_el.append(el)
    # Return link XML element
    return link_el


def __encode_joint_type(joint_type: str):
    match joint_type:
        case "fix":
            return "fixed"
        case "rev":
            return "revolute"
    return "fixed"


def generate_joint_name(joint_edge_name: str, reference_name: str):
    return __REI_KINEMATIC_ELEMENT_SEPARATOR.join([joint_edge_name, reference_name])


def default_joint_name(j1: HypergraphRelation, prefix: str = ""):
    jrel = [x for x in j1.get_subelements(lambda x: isinstance(x, KinematicJoint))][0]
    return join_w_prefix_separator([jrel.id_name], __REI_KINEMATIC_ELEMENT_SEPARATOR, prefix)


def joint_base_element(j0: HypergraphRelation, j1: HypergraphRelation, prefix=""):
    return joint_base_element_endpoint(j0, j1, default_joint_name(j1, prefix), j1.endpoint.id_name, prefix)


def joint_base_element_endpoint(j0, j1, joint_name: str, child_endpoint_name, prefix=""):
    joint_el = etree.Element("joint")
    # Joint elements
    # Parent
    el_joint_parent = etree.Element("parent")
    # Child
    el_joint_child = etree.Element("child")
    el_joint_child.text = join_w_prefix_separator([child_endpoint_name], __REI_KINEMATIC_ELEMENT_SEPARATOR, prefix)
    el_joint_parent.text = join_w_prefix_separator([j0.endpoint.id_name], __REI_KINEMATIC_ELEMENT_SEPARATOR, prefix)
    # Add joint parent-childs
    joint_el.append(el_joint_parent)
    joint_el.append(el_joint_child)
    # Kinematic joint
    jrel = [x for x in j1.get_subelements(lambda x: isinstance(x, KinematicJoint))][0]
    joint_el.attrib["name"] = joint_name
    # Type
    joint_el.attrib["type"] = __encode_joint_type(jrel["joint_type"])
    # Axis
    __axis = [0.0, 0.0, 1.0]
    if jrel['axis'] is not None:
        __axis = jrel['axis']
    el_axis = etree.Element("axis")
    el_axis_xyz = etree.Element("xyz")
    el_axis_xyz.text = f"{__axis[0]} {__axis[1]} {__axis[2]}"
    el_axis.append(el_axis_xyz)
    joint_el.append(el_axis)
    # Rigid transformation
    for x in jrel.get_subelements(lambda x: isinstance(x, RigidTransformation)):
        el_joint_pose = extract_rigid_transformation_element(x)
        el_joint_pose.attrib['relative_to'] = join_w_prefix_separator(
            [j0.endpoint.id_name], __REI_KINEMATIC_ELEMENT_SEPARATOR, prefix)
        # Add pose to joint
        joint_el.append(el_joint_pose)
    # Return joint element
    return joint_el
