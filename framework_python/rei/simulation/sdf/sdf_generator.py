from rei.cognitive.channels.cognitive_icons import TextfileCognitiveIcon
from rei.cognitive.entities.entity.cognitiveentity import CognitiveEntity
from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from rei.cognitive.channels.channel_base_definitions import CognitiveChannelDendrite

import os
from lxml import etree

from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphReferenceConnection, \
    select_incoming_connections
from rei.cognitive.format.hypergraph.foundations.hypergraph_operators import hypergraphedge_2factorization_tree
from rei.physics.geometry.basic_geometry import PolyhedronGeometry, EllipsoidGeometry, CylinderGeometry, \
    PrimitiveGeometry
from rei.physics.kinematics.kinematic_link import VisionGeometry, KinematicLink, WorldLink, CollisionGeometry, \
    KinematicJoint, KinematicJointType, KinematicGraph, GeometryNode
from rei.cognitive.format.hypergraph.lang.mapping.cogni_lang_mapping import load_system_from_description
from rei.simulation.mapping.material_map import GAZEBO_MATERIALS_DICT


__SDF_GEN_VERSION: str = "1.7"


class SdfGenerator(CognitiveChannelDendrite):

    def __init__(self, name: str, timestamp: int, e_root=None, domain=None, channel=None, icon=None) -> None:
        super().__init__(name, timestamp, domain, channel, icon)
        self.eval_cache = {}
        self.link_element_cache = {}
        if e_root is not None:
            self.e_root = e_root
        else:
            # Generate SDF
            root: etree.Element = etree.Element("sdf")
            root.attrib["version"] = "1.7"
            self.e_root = root
        self.ref_cognitive_entity = None

    @staticmethod
    def _setup_polyhedron_geometry_element(geom: PolyhedronGeometry):
        e_geom = etree.Element("box")
        e_size = etree.Element("size")
        e_size.text = f"{geom.dimensions[0]} {geom.dimensions[1]} {geom.dimensions[2]}"
        e_geom.append(e_size)
        return e_geom

    @staticmethod
    def _setup_ellipsoid_geometry_element(geom: EllipsoidGeometry):
        e_geom = etree.Element("sphere")
        e_radius = etree.Element("radius")
        e_radius.text = f"{geom.dimensions[0]}"
        e_geom.append(e_radius)
        return e_geom

    @staticmethod
    def _setup_cylinder_geometry_element(geom: CylinderGeometry):
        e_geom = etree.Element("cylinder")
        e_radius = etree.Element("radius")
        e_radius.text = f"{geom.dimensions[0]}"
        e_length = etree.Element("length")
        e_length.text = f"{geom.dimensions[1]}"
        e_geom.append(e_radius)
        e_geom.append(e_length)
        return e_geom

    @staticmethod
    def _setup_axis_element(child, e_joint: etree.Element):
        # Axis element
        el_axis = etree.Element("axis")
        el_axis_xyz = etree.Element("xyz")
        el_axis_xyz.text = f"{child.axis[0]} {child.axis[1]} {child.axis[2]}"
        el_axis.append(el_axis_xyz)
        e_joint.append(el_axis)

    @staticmethod
    def _setup_inertia(el: KinematicLink, e_link: etree.Element):
        # Inertia setup
        e_inertial = etree.Element("inertial")
        # Mass element
        e_mass = etree.Element("mass")
        e_mass.text = str(el.mass)
        # Inertia element
        e_inertia = etree.Element("inertia")
        e_ixx = etree.Element("ixx")
        e_ixx.text = str(el.inertia[0])
        e_inertia.append(e_ixx)
        e_iyy = etree.Element("iyy")
        e_iyy.text = str(el.inertia[1])
        e_inertia.append(e_iyy)
        e_izz = etree.Element("izz")
        e_izz.text = str(el.inertia[2])
        e_inertia.append(e_izz)
        e_ixy = etree.Element("ixy")
        e_ixy.text = str(el.inertia[3])
        e_inertia.append(e_ixy)
        e_ixz = etree.Element("ixz")
        e_ixz.text = str(el.inertia[4])
        e_inertia.append(e_ixz)
        e_iyz = etree.Element("iyz")
        e_iyz.text = str(el.inertia[5])
        e_inertia.append(e_iyz)
        e_inertial.append(e_inertia)
        # Add mass element
        e_inertial.append(e_mass)
        # Wrap up inertia
        e_link.append(e_inertial)

    @staticmethod
    def _setup_material_element(g: VisionGeometry, e_viz: etree.Element):
        if g.material_name is not None:
            e_material = etree.Element("material")
            # Gazebo specific
            e_script = etree.Element("script")
            e_source_uri = etree.Element("uri")
            e_source_uri.text = "file://media/materials/scripts/gazebo.material"
            e_script.append(e_source_uri)
            e_material_name = etree.Element("name")
            e_material_name.text = GAZEBO_MATERIALS_DICT[g.material_name]
            e_script.append(e_material_name)
            # Wrap up
            e_material.append(e_script)
            #
            e_viz.append(e_material)

    def setup_link(self, el: KinematicLink, e_entity: etree.Element,
                   template_name: str = "", evoker_name: str = ""):
        if not isinstance(el, WorldLink):
            e_link = etree.Element("link")
            # Handle template name
            link_name = el.id_name
            if template_name != "":
                link_name = template_name + "/" + link_name
            e_link.attrib["name"] = link_name
            e_entity.append(e_link)
            # Setup inertia
            SdfGenerator._setup_inertia(el, e_link)
            # Add link to cache
            self.link_element_cache[el.progenitor_registry.qualified_name] = e_link
            # Add link pose
            e_pose = etree.Element("pose")
            e_pose.text = el.str_pose()
            e_link.append(e_pose)
            self.link_element_cache[el.progenitor_registry.qualified_name + "/pose"] = e_pose
            if evoker_name != "":
                e_pose.attrib["relative_to"] = evoker_name
            # Setup geometry
            for g in el.subset_elements:
                match g:
                    case VisionGeometry():
                        e_viz = self.setup_geometry(g, e_link)
                        SdfGenerator._setup_material_element(g, e_viz)
                    case CollisionGeometry():
                        self.setup_geometry(g, e_link, tag="collision")

    def setup_geometry(self, geom: GeometryNode, e_link: etree.Element, tag="visual"):
        e_visual = etree.Element(tag)
        e_visual.attrib["name"] = geom.id_name
        e_geom = etree.Element("geometry")
        for s in geom.subset_elements:
            match s:
                case PrimitiveGeometry():
                    SdfGenerator.setup_geometry_element(s, e_geom)
                case HypergraphReferenceConnection():
                    if s.direction == EnumRelationDirection.OUTWARDS:
                        if s.parent.progenitor_registry.qualified_name not in self.eval_cache:
                            ref = select_incoming_connections(s.parent)[0]
                            self.eval_cache[s.parent.progenitor_registry.qualified_name] = ref.endpoint
                        ref = self.eval_cache[s.parent.progenitor_registry.qualified_name]
                        for _ref_geom in ref.subset_elements:
                            match _ref_geom:
                                case PrimitiveGeometry():
                                    SdfGenerator.setup_geometry_element(_ref_geom, e_geom)
            e_visual.append(e_geom)
        e_link.append(e_visual)
        return e_visual

    @staticmethod
    def setup_geometry_element(geom: PrimitiveGeometry, e_geomdef: etree.Element):
        e_geom = None
        match geom:
            case PolyhedronGeometry():
                e_geom = SdfGenerator._setup_polyhedron_geometry_element(geom)
            case EllipsoidGeometry():
                e_geom = SdfGenerator._setup_ellipsoid_geometry_element(geom)
            case CylinderGeometry():
                e_geom = SdfGenerator._setup_cylinder_geometry_element(geom)
        e_geomdef.append(e_geom)

    def setup_joint(self, el: KinematicJoint, e_entity: etree.Element,
                    template_name: str = ""):
        # 2 factorization for trees
        tree_connections = hypergraphedge_2factorization_tree(el)
        while not tree_connections.empty():
            # Ensure templating
            parent, child = tree_connections.get()
            e_joint = etree.Element("joint")
            # Handle template name
            joint_name = f"{el.id_name}/{child.endpoint.id_name}"
            jnt_parent_name = parent.endpoint.id_name
            jnt_child_name = child.endpoint.id_name
            if template_name != "":
                joint_name = template_name + "/" + joint_name
                jnt_parent_name = template_name + "/" + jnt_parent_name
                jnt_child_name = template_name + "/" + child.endpoint.id_name
            e_joint.attrib["name"] = joint_name
            # Set type
            match child.joint_type:
                case KinematicJointType.FIXED:
                    e_joint.attrib["type"] = "fixed"
                case KinematicJointType.REVOLUTE:
                    e_joint.attrib["type"] = "revolute"
                case KinematicJointType.PRISMATIC:
                    e_joint.attrib["type"] = "prismatic"
            # Pose element
            el_pose = etree.Element("pose")
            el_pose.text = f"{child.rigid_transformation[0][0]} {child.rigid_transformation[0][1]} " \
                           f"{child.rigid_transformation[0][2]} {child.rigid_transformation[1][0]} " \
                           f"{child.rigid_transformation[1][1]} {child.rigid_transformation[1][2]}"
            # Set joint relative to parent joint
            if parent.endpoint.id_name != "world":
                el_pose.attrib["relative_to"] = jnt_parent_name
            e_joint.append(el_pose)
            # Parent element
            el_parent = etree.Element("parent")
            el_parent.text = jnt_parent_name
            e_joint.append(el_parent)
            # Child element
            if isinstance(child.endpoint, KinematicGraph):
                el_child = etree.Element("child")
                el_child.text = el.id_name+"/"+child.endpoint.root_link.id_name
                e_joint.append(el_child)
                self.instantiate_kinematic_graph(child.endpoint, e_entity, el.id_name, joint_name)
            else:
                el_child = etree.Element("child")
                el_child.text = jnt_child_name
                e_joint.append(el_child)
                # Set child link pose relative to joint
                if parent.endpoint.id_name != "world":
                    self.link_element_cache[child.endpoint.progenitor_registry.qualified_name + "/pose"].attrib[
                        "relative_to"] = joint_name
            SdfGenerator._setup_axis_element(child, e_joint)
            e_entity.append(e_joint)

    def instantiate_kinematic_graph(self, _el: KinematicGraph, e_entity: etree.Element,
                                    template_name: str = "", evoker_name: str = ""):
        for el in _el.subset_elements:
            match el:
                case KinematicLink():
                    self.setup_link(el, e_entity, template_name, evoker_name)
                case KinematicJoint():
                    self.setup_joint(el, e_entity, template_name)

    def setup_cognitive_entity(self, n: CognitiveEntity):
        e_entity = etree.Element("model")
        e_entity.attrib["name"] = n.id_name
        self.e_root.append(e_entity)
        self.ref_cognitive_entity = n
        #
        for _el in filter(lambda x: isinstance(x, KinematicGraph), self.ref_cognitive_entity.subset_elements):
            # Go only one level down
            self.instantiate_kinematic_graph(_el, e_entity)

    def encode(self, arg):
        self.setup_cognitive_entity(arg)
        if self.endpoint is not None:
            self.endpoint.update((self.ref_cognitive_entity, self.e_root))

    def decode(self, arg):
        # TODO: implement it... somehow (e.g., XSLT)
        pass


class ElementTreeCognitiveIcon(TextfileCognitiveIcon):

    def _write_to_file(self, filename: str):
        etree.ElementTree(self.buffer_msg[1]).write(filename+".sdf", pretty_print=True)
        with open(filename+".load.sh", 'w+') as f:
            f.write(f"ros2 run gazebo_ros spawn_entity.py -entity {self.buffer_msg[0].id_name} "
                    f"-file {self.buffer_msg[0].id_name}.sdf")
        os.chmod(filename+".load.sh", 0o777)

    def update(self, msg: tuple):
        super().update(msg)


def load_from_description(filename: str, output_dir: str):
    sys, channel = load_system_from_description(filename)
    # Class SDF generator
    sdf_gen = SdfGenerator("loader", 0, domain=sys.domain, channel=channel)

    for n in sys.subset_elements:
        if isinstance(n, CognitiveEntity):
            # Check directory structure
            target_dir = '/'.join([output_dir, n.id_name])
            if not os.path.isdir(target_dir):
                os.makedirs(target_dir)
            # Create cognitive icon
            icon = ElementTreeCognitiveIcon("sdf_out", 0, target_dir)
            # Add cognitive icon to channel
            channel.add_connection(sdf_gen, 0, icon)
            # Load from description
            sdf_gen.encode(n)
            # Yield loaded description
            yield sys, channel, icon
