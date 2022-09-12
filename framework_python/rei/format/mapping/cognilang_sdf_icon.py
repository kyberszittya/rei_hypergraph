import lxml
import numpy as np
from lxml import etree

from rei.format.semantics.CognitiveEntity import KinematicJoint, KinematicLink, CognitiveEntity, RigidTransformation, \
    VisualMaterial, GeometryNode, CylinderGeometry, EllipsoidGeometry
from rei.hypergraph.base_elements import HypergraphNode, HypergraphPort
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.factorization_operations import Factorization2SubsetOperation, RelationFactorization2SubsetOperation


class CognilangSdfIcon(object):

    def __init__(self):
        self.root_xml: etree.Element = etree.Element("sdf", attrib={"version":"1.7"})
        self.current_model = None
        self.cache = []

    def __add_model_element(self, element):
        # Wrap-up
        if self.current_model is None:
            self.cache.append(element)
        else:
            self.current_model.append(element)

    def __extract_geometry_element(self, element):
        for e in element.get_subelements(lambda x: isinstance(x, GeometryNode)):
            geometry = etree.Element("geometry")
            el_geom = None
            match e:
                case CylinderGeometry():
                    el_geom = etree.Element("cylinder")
                    el_radius = etree.Element("radius")
                    el_radius.text = str(e["values"][0])
                    el_length = etree.Element("length")
                    el_length.text = str(e["values"][1])
                    el_geom.append(el_radius)
                    el_geom.append(el_length)
                case EllipsoidGeometry():
                    if len(e["values"]) == 1:
                        el_geom = etree.Element("sphere")
                        el_radius = etree.Element("radius")
                        el_radius.text = str(e["values"][0])
                        el_geom.append(el_radius)
                    else:
                        el_geom = etree.Element("ellipsoid")
                        el_radii = etree.Element("radii")
                        el_radii.text = ' '.join([str(x) for x in  e["values"]])
                        el_geom.append(el_radii)
            if el_geom is not None:
                geometry.append(el_geom)
            yield geometry

    def encode_element(self, element):
        match element:
            case KinematicLink():
                element: KinematicLink
                link_el = etree.Element("link")
                link_el.attrib["name"] = element.id_name
                #
                cont_node: HypergraphNode = element.parent
                # Check relative frame
                relative_frame_name = None
                for x in cont_node.sub_ports:
                    x: HypergraphPort
                    subel = [r for r in x.endpoint.get_subelements(lambda y: isinstance(y, KinematicJoint))]
                    if x.endpoint.direction == EnumRelationDirection.INWARDS and len(subel)>0:
                        relative_frame_name = subel[0].id_name
                # Rigid transformation
                for x in element.get_subelements(lambda x: isinstance(x, RigidTransformation)):
                    el_joint_pose = self.__extract_rigid_transformation_element(x)
                    # Check relative frame
                    if relative_frame_name is not None:
                        el_joint_pose.attrib["relative_to"] = relative_frame_name
                    # Add pose to joint
                    link_el.append(el_joint_pose)
                # Visual & collision geometry setup
                sub_nodes = [x for x in cont_node.get_subelements(lambda x: isinstance(x, HypergraphNode))]
                __sem_collision = []
                __sem_visual = []
                __sem_material = {}
                for n in sub_nodes:
                    geometries = [x for x in n.get_subelements(lambda x: isinstance(x, HypergraphNode))]
                    mat = [x for x in n.get_subelements(lambda x: isinstance(x, VisualMaterial))]
                    if len(mat) != 0:
                        __sem_visual.extend(geometries)
                        __sem_material = ({i: mat[0] for i in geometries})
                    else:
                        __sem_collision.extend(geometries)
                # Visual geometry setup
                for __v in __sem_visual:
                    el_visual = etree.Element("visual")
                    el_visual.attrib["name"] = __v.id_name
                    for __x in self.__extract_geometry_element(__v):
                        el_visual.append(__x)
                    link_el.append(el_visual)
                    # Material
                    el_material = etree.Element("material")
                    el_script = etree.Element("script")
                    el_script_uri = etree.Element("uri")
                    el_script_uri.text = "file://media/materials/scripts/gazebo.material"
                    el_material_name = etree.Element("name")
                    el_material_name.text = __sem_material[__v]["material_name"]
                    el_script.append(el_script_uri)
                    el_script.append(el_material_name)
                    el_material.append(el_script)
                    el_visual.append(el_material)
                # Collision geometry setup
                for __c in __sem_collision:
                    el_coll = etree.Element("collision")
                    self.__extract_geometry_element(__c)
                    for __x in self.__extract_geometry_element(__c):
                        el_coll.append(__x)
                    link_el.append(el_coll)
                # Add link to current model
                self.__add_model_element(link_el)
            case CognitiveEntity():
                element: CognitiveEntity
                model_el = etree.Element("model")
                self.root_xml.append(model_el)
                self.current_model = model_el
                if len(self.cache) > 0:
                    for e in self.cache:
                        self.current_model.append(e)
                    self.cache = []
            case KinematicJoint():
                element: KinematicJoint
                joint_el = etree.Element("joint")
                self.__add_model_element(joint_el)

    def __extract_rigid_transformation_element(self, x: RigidTransformation):
        el_pose = etree.Element("pose")
        rot = [x for x in x['rotation']]
        match x['rotation_type']:
            case 'deg':
                rot = [180.0/np.pi*x for x in rot]
        el_pose.text = f"{x['translation'][0]} {x['translation'][1]} {x['translation'][2]} {rot[0]} {rot[1]} {rot[2]}"
        # Set relative frame
        return el_pose

    async def encode(self, elements):
        cognitive_entities = filter(lambda x: isinstance(x, CognitiveEntity), elements)
        # Cognitive elements
        for i in cognitive_entities:
            self.encode_element(i)
        # Nodes
        links = filter(lambda x: isinstance(x, KinematicLink), elements)
        for i in links:
            self.encode_element(i)
        # Joint subset factorization
        __selected_elements = [x.parent for x in filter(lambda x: isinstance(x, KinematicLink), elements)]
        __selected_elements.extend([x.parent for x in filter(lambda x0: isinstance(x0, KinematicJoint), elements)])
        # Query
        query = RelationFactorization2SubsetOperation()
        joints = await query.execute(__selected_elements)
        for j in joints:
            joint_el = etree.Element("joint")
            # Joint elements
            # Parent
            el_joint_parent = etree.Element("parent")
            el_joint_parent.text = j[0].endpoint.id_name
            # Child
            el_joint_child = etree.Element("child")
            el_joint_child.text = j[1].endpoint.id_name
            # Kinematic joint
            jrel = [x for x in j[1].get_subelements(lambda x: isinstance(x, KinematicJoint))][0]
            joint_el.attrib["name"] = jrel.id_name
            # Type
            joint_el.attrib["type"] = jrel["joint_type"]
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
                el_joint_pose = self.__extract_rigid_transformation_element(x)
                el_joint_pose.attrib['relative_to'] = j[0].endpoint.id_name
                # Add pose to joint
                joint_el.append(el_joint_pose)
            # Add joint
            joint_el.append(el_joint_parent)
            joint_el.append(el_joint_child)
            self.__add_model_element(joint_el)
