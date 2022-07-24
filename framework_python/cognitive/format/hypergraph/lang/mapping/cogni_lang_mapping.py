from antlr4 import FileStream, CommonTokenStream

from cognitive.entities.entity.cognitiveentity import CognitiveEntity, ParameterNode
from cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from cognitive.format.hypergraph.channels.tensor_channel import CognitiveChannel, CognitiveArbiter, \
    CognitiveChannelDendrite
from cognitive.format.hypergraph.foundations.common_mappings import map_graph_direction
from cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphReferenceConnection, \
    HypergraphNode, select_incoming_connections
from cognitive.format.hypergraph.foundations.hypergraph_operators import create_hypergraphelement_reference, \
    hypergraphedge_2factorization_tree
from cognitive.format.hypergraph.lang.cognilang.CogniLangLexer import CogniLangLexer
from cognitive.format.hypergraph.lang.cognilang.CogniLangParser import CogniLangParser
from cognitive.format.hypergraph.lang.cognilang.CogniLangVisitor import CogniLangVisitor
from cognitive.format.hypergraph.lang.mapping.graphviz_mapping import create_graph_view
from cognitive.format.hypergraph.lang.mapping.material_map import GAZEBO_MATERIALS_DICT
from cognitive.physics.geometry.basic_geometry import CylinderGeometry, PolyhedronGeometry, EllipsoidGeometry, \
    PrimitiveGeometry
from cognitive.physics.kinematics.kinematic_link import KinematicLink, KinematicJoint, VisionGeometry, \
    CollisionGeometry, KinematicJointType, connect_joint_to_node, GeometryNode, WorldLink, KinematicGraph, \
    get_joint_type_from_antlr_relation
from lxml import etree


import numpy as np


class EntityGraphMapper(CogniLangVisitor):

    def __init__(self, channel: CognitiveChannel, arbiter: CognitiveArbiter):
        super().__init__()
        self.arbiter = arbiter
        self.channel = channel
        self.rootentity: [CognitiveEntity | None] = None
        self.kinematic_graph_cache = {}

    def visitEntity(self, ctx: CogniLangParser.EntityContext):
        name = str(ctx.graphnode_signature().ID())
        self.rootentity = CognitiveEntity(name, 0)
        self.arbiter.add_subset(self.rootentity, 0)
        #
        return self.visitChildren(ctx)

    @staticmethod
    def _float_vector_to_numpy(root: CognitiveEntity, vector: CogniLangParser.Field_float_vectorContext):
        values = []
        for a in vector.float_vector().value():
            if a.FLOAT() is not None:
                values.append(float(str(a.FLOAT())))
            elif a.ref_() is not None:
                values.append(float(root.get_parameter(str(a.ref_().ID())).value))
        return np.array(values)

    def _setup_geometry(self, name: str, geom: HypergraphNode, context: KinematicGraph, v):
        # Check if the geometries are reference to other elements
        if v.geometry_body().geometries().ref_() is not None:
            geom_ref_name = f"{v.geometry_body().geometries().ref_().ID()}"
            create_hypergraphelement_reference(geom_ref_name, context, geom)
        else:
            _geom = None
            if v.geometry_body().geometries().cylinder_geometry() is not None:
                _geom = CylinderGeometry(f"geom_{name}", 0, EntityGraphMapper._float_vector_to_numpy(
                    self.rootentity,
                    v.geometry_body().geometries().cylinder_geometry().field_float_vector()
                ))
            elif v.geometry_body().geometries().polyhedron_geometry() is not None:
                _geom = PolyhedronGeometry(f"geom_{name}", 0, EntityGraphMapper._float_vector_to_numpy(
                    self.rootentity,
                    v.geometry_body().geometries().polyhedron_geometry().field_float_vector()
                ))
            elif v.geometry_body().geometries().ellipsoid_geometry() is not None:
                _geom = EllipsoidGeometry(f"geom_{name}", 0, EntityGraphMapper._float_vector_to_numpy(
                    self.rootentity,
                    v.geometry_body().geometries().ellipsoid_geometry().field_float_vector()
                ))
            geom.add_subset(_geom, 0)

    def _viz_geom_setup(self, name: str, element: HypergraphNode, context: KinematicGraph, prefix: str, arg):
        for v in arg:
            e_material = None
            if v.material() is not None:
                e_material = v.material().material_name.text
            viz_name = v.ID()
            if viz_name is None:
                viz_name = '_'.join([prefix, name])
            else:
                viz_name = str(viz_name)
            viz = VisionGeometry(viz_name, 0, material_name=e_material)
            element.add_subset(viz, 0)
            self._setup_geometry(viz_name, viz, context, v)

    def _coll_geom_setup(self, name: str, element: HypergraphNode, context: KinematicGraph, prefix: str, arg):
        for v in arg:
            coll_name = v.ID()
            if coll_name is None:
                coll_name = '_'.join([prefix, name])
            else:
                coll_name = str(coll_name)
            coll = CollisionGeometry(coll_name, 0)
            element.add_subset(coll, 0)
            self._setup_geometry(coll_name, coll, context, v)

    def visitKinematic(self, ctx: CogniLangParser.KinematicContext):
        gr: KinematicGraph = KinematicGraph(str(ctx.graphnode_signature().ID()), 0)
        self.kinematic_graph_cache[str(ctx.graphnode_signature().ID())] = gr
        _, pt = self._retrieve_current_kinematic_graph(ctx)
        if pt is None:
            self.rootentity.add_kinematic_graph(gr, 0)
        else:
            pt.add_kinematic_graph(gr, 0)
        # Setup a mock world link
        gr.add_subset(WorldLink("world", 0), 0)
        return self.visitChildren(ctx)

    def _retrieve_current_kinematic_graph(self, ctx):
        # Retrieve name of the kinematicgraph
        if isinstance(ctx.parentCtx.parentCtx, CogniLangParser.Entity_subset_elemContext):
            return None, None
        parent_ctx_name = str(ctx.parentCtx.parentCtx.graphnode_signature().ID())
        context: KinematicGraph = self.kinematic_graph_cache[parent_ctx_name]
        return parent_ctx_name, context

    def visitLink(self, ctx: CogniLangParser.LinkContext):
        # Retrieve name of the kinematicgraph
        _, context = self._retrieve_current_kinematic_graph(ctx)
        # Get the name of the current link
        name = str(ctx.graphnode_signature().ID())
        body: CogniLangParser.Linknode_bodyContext = ctx.linknode_body()
        pose = None
        if ctx.pose is not None:
            pose = EntityGraphMapper._float_vector_to_numpy(self.rootentity, ctx.pose)
        mass = float(body.inertia_body().mass.text)
        link = KinematicLink(name, 0, mass=mass, pose=pose)
        context.add_subset(link, 0)
        if ctx.root_link is not None:
            context.set_root_link(link)
        self._viz_geom_setup(name, link, context, 'viz', body.visual_node())
        self._coll_geom_setup(name, link, context, 'coll', body.collision_node())
        # Setup inertia
        if body.inertia_body().inertia_vector() is not None:
            EntityGraphMapper._float_vector_to_numpy(context, body.inertia_body().inertia_vector().inertia_vector_)
        else:
            # If no inertia vector is defined, try to calculate it
            for v in filter(lambda x: isinstance(x, CollisionGeometry), link.subset_elements):
                for g in v.subset_elements:
                    for ref in filter(lambda x: isinstance(x, HypergraphReferenceConnection), g.parent.subset_elements):
                        if ref.direction == EnumRelationDirection.INWARDS:
                            # TODO: revise inertia calculation
                            for inert in filter(lambda x: isinstance(x, PrimitiveGeometry),
                                                ref.endpoint.subset_elements):
                                link.calc_explicit_primitive_inertia(inert)
        # Wrap-up
        return self.visitChildren(ctx)

    @staticmethod
    def generate_rotation(transformation: CogniLangParser.Rigid_transformationContext):
        if transformation.rotation() is not None:
            rot: CogniLangParser.RotationContext = transformation.rotation()
            if rot.rot_type is not None:
                match rot.rot_type.text:
                    case 'd':
                        return [float(str(x.FLOAT())) * np.pi / 180.0 for x in rot.float_vector().value()]
                    case 'r':
                        return [float(str(x.FLOAT())) for x in rot.float_vector().value()]
            else:
                return [float(str(x.FLOAT())) for x in rot.float_vector().value()]
        else:
            return [0.0, 0.0, 0.0]

    def visitParameter(self, ctx: CogniLangParser.ParameterContext):
        value = None
        if ctx.INT() is not None:
            value = int(ctx.parameter_value)
        elif ctx.FLOAT() is not None:
            value = float(ctx.parameter_value.text)
        param: ParameterNode = ParameterNode(ctx.name.text, value, 0)
        self.rootentity.add_parameter(param)

        return self.visitChildren(ctx)

    def visitJoint(self, ctx: CogniLangParser.JointContext):
        _, context = self._retrieve_current_kinematic_graph(ctx)
        name = str(ctx.graphedge_signature().ID())
        joint = KinematicJoint(name, 0, self.rootentity)
        body: CogniLangParser.Joint_bodyContext = ctx.joint_body()
        for rel in body.joint_relation():
            target_name = str(rel.ref_().ID())
            t: KinematicJointType = get_joint_type_from_antlr_relation(rel)
            # Rigid transformation setup
            tr = None
            if rel.rigid_transformation() is not None:
                tr = np.array([
                    [float(str(x.FLOAT())) for x in rel.rigid_transformation().float_vector().value()],
                    EntityGraphMapper.generate_rotation(rel.rigid_transformation())
                ])
            # Type setup
            joint.joint_type = t
            direction: EnumRelationDirection = map_graph_direction(rel)
            # Axis setup
            axis = None
            if rel.axis() is not None:
                axis = np.array([float(str(x.FLOAT())) for x in rel.axis().float_vector().value()])
            connect_joint_to_node(context, 0, joint, t, tr, axis, target_name, direction)
        context.add_subset(joint, 0)
        # Return
        return self.visitChildren(ctx)


class SdfGenerator(CognitiveChannelDendrite):

    def __init__(self, name: str, timestamp: int, e_root=None, domain=None, channel=None, icon=None) -> None:
        super().__init__(name, timestamp, domain, channel, icon)
        self.eval_cache = {}
        self.link_element_cache = {}
        self.e_root = e_root
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

    def write_to_file(self):
        etree.ElementTree(self.e_root).write(f"{self.ref_cognitive_entity.id_name}.sdf", pretty_print=True)

    def encode(self, arg):
        if arg is None:
            self.write_to_file()

    def decode(self, arg):
        # TODO: implement it... somehow (e.g., XSLT)
        pass


def load_system_from_description(filename: str, verbose=True):
    sys = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_desc", 0, sys)
    # Parse language
    stream = FileStream(filename)
    lexer = CogniLangLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = CogniLangParser(stream)
    tree = parser.rootnode()
    # Instantiate visitor
    visitor = EntityGraphMapper(channel, sys)
    visitor.visit(tree)
    if verbose:
        visitor.rootentity.print_hierarchy_tree()
    return sys, channel


def load_from_description(filename: str):
    sys, channel = load_system_from_description(filename)
    # Generate SDF
    root: etree.Element = etree.Element("sdf")
    root.attrib["version"] = "1.7"
    # Class SDF generator
    sdf_gen = SdfGenerator("loader", 0, root, sys.domain, channel)
    for n in sys.subset_elements:
        if isinstance(n, CognitiveEntity):
            sdf_gen.setup_cognitive_entity(n)
    sdf_gen.write_to_file()
    return sys, channel


def main():
    # TODO: ambient description (very-very important, by this point it would be awesome)
    sys, channel = load_from_description("D:\\Haizu\\robotics_ws\\cogni_ws\\rei_ws\\rei\\framework_python\\cognitive\\format\\hypergraph\\lang\\examples\\example_robotcar.cogni")
    create_graph_view(sys)


if __name__ == "__main__":
    main()
