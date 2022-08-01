from antlr4 import FileStream, CommonTokenStream

from rei.cognitive.ambience.elements.definitive_elements import AmbientGraph, SensorElement, ExteroceptiveSensor, \
    AmbienceEdge, CommunicationPort, AmbienceCommunicationConnection
from rei.cognitive.ambience.graph_operations import connect_ambience_to_port
from rei.cognitive.entities.entity.cognitiveentity import CognitiveEntity, ParameterNode
from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from rei.cognitive.channels.channel_base_definitions import CognitiveChannel, CognitiveArbiter
from rei.cognitive.format.hypergraph.foundations.common_mappings import map_graph_direction, map_communication_type
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphReferenceConnection, \
    HypergraphNode
from rei.cognitive.format.hypergraph.lang.cognilang.framework.cognitive.speclanguage.src.main.antlr4.CogniLangLexer import \
    CogniLangLexer
from rei.cognitive.format.hypergraph.lang.cognilang.framework.cognitive.speclanguage.src.main.antlr4.CogniLangParser import \
    CogniLangParser
from rei.cognitive.format.hypergraph.lang.cognilang.framework.cognitive.speclanguage.src.main.antlr4.CogniLangVisitor import \
    CogniLangVisitor
from rei.cognitive.format.hypergraph.operations.generative_operators import create_hypergraphelement_reference
from rei.physics.geometry.basic_geometry import CylinderGeometry, PolyhedronGeometry, EllipsoidGeometry, \
    PrimitiveGeometry
from rei.physics.kinematics.kinematic_link import KinematicLink, KinematicJoint, VisionGeometry, \
    CollisionGeometry, KinematicJointType, connect_joint_to_node, WorldLink, KinematicGraph, \
    get_joint_type_from_antlr_relation

import numpy as np


class EntityGraphMapper(CogniLangVisitor):

    def __init__(self, channel: CognitiveChannel, arbiter: CognitiveArbiter):
        super().__init__()
        self.arbiter = arbiter
        self.channel = channel
        self.rootentity: [CognitiveEntity | None] = None
        self.kinematic_graph_cache = {}
        self.ambient_graph_cache = {}
        self.ports_cache = {}

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

    def _retrieve_current_ambient_graph(self, ctx):
        _ctx = ctx.parentCtx.parentCtx.parentCtx
        # Retrieve name of the kinematicgraph
        if isinstance(_ctx, CogniLangParser.Entity_subset_elemContext):
            return None, None
        parent_ctx_name = str(_ctx.graphnode_signature().ID())
        context: AmbientGraph = self.ambient_graph_cache[parent_ctx_name]
        return parent_ctx_name, context

    def _geometry_setup(self, name: str, link, context: KinematicGraph, body):
        self._viz_geom_setup(name, link, context, 'viz', body.visual_node())
        self._coll_geom_setup(name, link, context, 'coll', body.collision_node())

    @staticmethod
    def _inertia_element_geometry_setup(link: KinematicLink):
        # If no inertia vector is defined, try to calculate it
        for v in filter(lambda x: isinstance(x, CollisionGeometry), link.subset_elements):
            for g in v.subset_elements:
                for ref in filter(lambda x: isinstance(x, HypergraphReferenceConnection), g.parent.subset_elements):
                    if ref.direction == EnumRelationDirection.INWARDS:
                        # TODO: revise inertia calculation
                        for inert in filter(lambda x: isinstance(x, PrimitiveGeometry),
                                            ref.endpoint.subset_elements):
                            link.calc_explicit_primitive_inertia(inert)

    def visitLink(self, ctx: CogniLangParser.LinkContext):
        """
        Link visitor function

        :param ctx:
        :return:
        """
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
        if ctx.root_link is not None:
            context.set_root_link(link)
        context.add_subset(link, 0)
        self._geometry_setup(name, link, context, body)
        # Setup inertia
        if body.inertia_body().inertia_vector() is not None:
            EntityGraphMapper._float_vector_to_numpy(context, body.inertia_body().inertia_vector().inertia_vector_)
        else:
            EntityGraphMapper._inertia_element_geometry_setup(link)
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

    def visitAmbient(self, ctx: CogniLangParser.AmbientContext):
        name = str(ctx.graphnode_signature().ID())
        ag = AmbientGraph(name, 0)
        self.ambient_graph_cache[name] = ag
        self.rootentity.add_subset(ag, 0)
        return self.visitChildren(ctx)

    def visitSensor(self, ctx: CogniLangParser.SensorContext):
        _, _parent_ambient_graph = self._retrieve_current_ambient_graph(ctx)
        sensor_name = str(ctx.ambient_element_signature().ID())
        if ctx.sensor_type().proprioceptive_sensor() is not None:
            print("Proprioceptive sensor")
        elif ctx.sensor_type().exteroceptive_sensor() is not None:
            ext_sensor_type: CogniLangParser.Ext_sensor_typeContext = \
                str(ctx.sensor_type().exteroceptive_sensor().ext_sensor_type())
            se: ExteroceptiveSensor = ExteroceptiveSensor(sensor_name, 0)
            _parent_ambient_graph.add_subset(se, 0)
        return self.visitChildren(ctx)

    def visitActuator(self, ctx: CogniLangParser.ActuatorContext):
        print(ctx.ambient_element_signature().ID())
        return self.visitChildren(ctx)

    def visitPort(self, ctx: CogniLangParser.PortContext):
        _, parent_ambient_graph = self._retrieve_current_ambient_graph(ctx)
        port_name = str(ctx.port_signature().graphnode_signature().ID())
        topic_name: str = str(ctx.port_signature().topic_name)
        msg_type: str = str(ctx.port_signature().msg)
        port: CommunicationPort = CommunicationPort(port_name, 0, topic_name, msg_type)
        parent_ambient_graph.add_subset(port, 0)
        self.ports_cache[port_name] = port
        return self.visitChildren(ctx)

    def visitAmbience_edge(self, ctx: CogniLangParser.Ambience_edgeContext):
        _, _parent_ambient_graph = self._retrieve_current_ambient_graph(ctx)
        edge_name: str = str(ctx.graphedge_signature().ID())
        edge = AmbienceEdge(edge_name, 0, _parent_ambient_graph)
        for e in ctx.ambience_edge_body():
            for comm in e.communication_connections():
                direction = map_graph_direction(comm)
                target_name = str(comm.ref_().ID())
                comm_type = map_communication_type(comm)
                connect_ambience_to_port(_parent_ambient_graph, 0, edge, comm_type, target_name, direction)
            for placement in e.element_placement_relation():
                placement.geom_relation()
        _parent_ambient_graph.add_subset(edge, 0)
        return self.visitChildren(ctx)


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
