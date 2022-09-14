import numpy as np

from rei.format.phys.solid_geometry_context import encode_geometry_element
from rei.format.semantics.CognitiveEntity import RigidTransformation, KinematicLink, KinematicJoint, InertiaElement
from lxml import etree

from rei.hypergraph.base_elements import HypergraphPort, HypergraphNode, HypergraphEdge
from rei.hypergraph.common_definitions import EnumRelationDirection


__DEFAULT_RIGID_TRANSFORMATION = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def extract_rigid_transformation_element(x: RigidTransformation):
    el_pose = etree.Element("pose")
    rot = [x for x in x['rotation']]
    match x['rotation_type']:
        case 'deg':
            rot = [180.0/np.pi*x for x in rot]
    el_pose.text = f"{x['translation'][0]} {x['translation'][1]} {x['translation'][2]} {rot[0]} {rot[1]} {rot[2]}"
    # Set relative frame
    return el_pose


def __default_rigid_transformation_element():
    el_pose = etree.Element("pose")
    el_pose.text = ' '.join([str(x) for x in __DEFAULT_RIGID_TRANSFORMATION])
    # Set relative frame
    return el_pose


def encode_link_element(element: KinematicLink, prefix=""):
    link_el = etree.Element("link")
    if len(prefix) > 0:
        link_el.attrib["name"] = f"{prefix}.{element.id_name}"
    else:
        link_el.attrib["name"] = element.id_name
    #
    cont_node: HypergraphNode = element.parent
    # Check relative frame
    relative_frame_name = None
    for x in cont_node.sub_ports:
        x: HypergraphPort
        sub_el = [r for r in x.endpoint.get_subelements(lambda y: isinstance(y, KinematicJoint))]
        if x.endpoint.direction == EnumRelationDirection.OUTWARDS and len(sub_el)>0:
            e: HypergraphEdge = x.endpoint.parent
            incom = list(filter(lambda _r: _r.endpoint.id_name != "world", e.get_incoming_relations()))
            if len(incom) > 0:
                relative_frame_name = sub_el[0].id_name
    # Inertia
    # TODO: finish it
    for x in element.get_subelements(lambda x: isinstance(x, InertiaElement)):
        print("inert")
    # Rigid transformation
    for x in element.get_subelements(lambda x: isinstance(x, RigidTransformation)):
        el_joint_pose = extract_rigid_transformation_element(x)
        # Check relative frame
        if relative_frame_name is not None:
            el_joint_pose.attrib["relative_to"] = relative_frame_name
        # Add pose to joint
        link_el.append(el_joint_pose)
        break
    else:
        el_joint_pose = __default_rigid_transformation_element()
        # Check relative frame
        if relative_frame_name is not None:
            el_joint_pose.attrib["relative_to"] = relative_frame_name
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


def joint_base_element(j0, j1, prefix=""):
    return joint_base_element_endpoint(j0, j1, j1.endpoint.id_name, prefix)

def joint_base_element_endpoint(j0, j1, child_endpoint_name, prefix=""):
    joint_el = etree.Element("joint")
    # Joint elements
    # Parent
    el_joint_parent = etree.Element("parent")
    # Child
    el_joint_child = etree.Element("child")
    if len(prefix) == 0:
        el_joint_child.text = child_endpoint_name
        el_joint_parent.text = j0.endpoint.id_name
    else:
        el_joint_child.text = f"{prefix}.{child_endpoint_name}"
        el_joint_parent.text = f"{prefix}.{j0.endpoint.id_name}"
    # Add joint parent-childs
    joint_el.append(el_joint_parent)
    joint_el.append(el_joint_child)
    # Kinematic joint
    jrel = [x for x in j1.get_subelements(lambda x: isinstance(x, KinematicJoint))][0]
    if len(prefix) == 0:
        joint_el.attrib["name"] = jrel.id_name
    else:
        joint_el.attrib["name"] = f"{prefix}.{jrel.id_name}"
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
        if len(prefix) == 0:
            el_joint_pose.attrib['relative_to'] = j0.endpoint.id_name
        else:
            el_joint_pose.attrib['relative_to'] = '.'.join([prefix, j0.endpoint.id_name])
        # Add pose to joint
        joint_el.append(el_joint_pose)
    # Return joint element
    return joint_el