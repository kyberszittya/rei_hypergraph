from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.cognilang.CogniLangVisitor import CogniLangVisitor
from rei.format.mapping.cognilang_mapping_errors import ErrorParserNoFactorySet
from rei.format.mapping.cognilang_map_utility import extract_graphelement_signature, dir_enum_relation
from rei.format.phys.kinematics.kinematic_antlr_mapping import KinematicGraphContextMapper
from rei.format.semantics.CognitiveEntity import KinematicJoint, SensorPlacement, AmbiencePortCommunication
from rei.foundations.clock import MetaClock
from rei.hypergraph.common_definitions import EnumRelationDirection

__DEFAULT_ROTATION_LIST = [0.0, 0.0, 0.0]


class CognilangParserFileIcon(KinematicGraphContextMapper, CogniLangVisitor):

    def __init__(self, icon_name: str, clock: MetaClock):
        super().__init__(icon_name, clock)
        self.__root_entity = None

    @property
    def root_entity(self):
        return self.__root_entity

    #
    # SECTION: visitor overrides
    #

    def visitParameter(self, ctx:CogniLangParser.ParameterContext):
        if self._element_cache[self._generate_parent_node_name(ctx)] is self.__root_entity:
            self._factory.create_value(self._parameters, ctx.name.text, [ctx.parameter_value.text])
        return self.visitChildren(ctx)

    def visitRootnode(self, ctx: CogniLangParser.RootnodeContext):
        if self._factory is None:
            raise ErrorParserNoFactorySet
        return self.visitChildren(ctx)

    def visitEntity(self, ctx: CogniLangParser.EntityContext):
        name = str(ctx.graphnode_signature().ID())
        # Create entity as hypergraph
        _n = self._factory.generate_node(name, None)
        self.__root_entity = _n
        self._cognitive_element_factory.generate_semantic_element(
            'cognitiveentity', name, self.__root_entity, {'name': name})
        self._element_cache[_n.qualified_name] = _n
        # Return to context
        return self.visitChildren(ctx)

    def visitKinematic(self, ctx: CogniLangParser.KinematicContext):
        name = extract_graphelement_signature(ctx.graphnode_signature())
        parent_name = self._generate_parent_node_name(ctx)
        _el = self._factory.generate_node(name, self._element_cache[parent_name])
        self._cognitive_element_factory.generate_semantic_element('kinematicgraph', name, _el, {'name': name})
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)

    def visitVisual_node(self, ctx: CogniLangParser.Visual_nodeContext):
        _parent = self._generate_parent_node_name(ctx)
        _name = str(ctx.ID())
        # Create node
        _el = self._factory.generate_node(_name, self._element_cache[_parent])
        self._element_cache[_el.qualified_name] = _el
        # Extract geometry elements
        self._collect_geometries(ctx.geometry_body(), _el)
        self._collect_materials(ctx.material(), _el)
        return self.visitChildren(ctx)

    def visitCollision_node(self, ctx: CogniLangParser.Collision_nodeContext):
        _parent = self._generate_parent_node_name(ctx)
        if ctx.ID() is None:
            _name = "/".join([_parent, "coll"])
        else:
            _name = str(ctx.ID())
        # Create node
        _el = self._factory.generate_node(_name, self._element_cache[_parent])
        self._element_cache[_el.qualified_name] = _el
        # Extract geometry elements
        self._collect_geometries(ctx.geometry_body(), _el)
        return self.visitChildren(ctx)

    def visitLink(self, ctx: CogniLangParser.LinkContext):
        name = extract_graphelement_signature(ctx.graphnode_signature())
        parent_name = self._generate_parent_node_name(ctx)
        parent = self._element_cache[parent_name]
        _el = self._factory.generate_node(name, parent)
        # Kinematic link
        __sv = self._cognitive_element_factory.generate_semantic_element('kinematiclink', name, _el, {'name': name})
        # Rigid transformation
        __sv_trans = self._extract_rigid_transformation_element(ctx, __sv)
        if __sv_trans is not None:
            __sv.add_named_attribute('rigidtransformation', __sv_trans)
        # Inertia
        # Add element to cache
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)

    def visitJoint(self, ctx: CogniLangParser.JointContext):
        name = extract_graphelement_signature(ctx.graphedge_signature())
        parent_name = self._generate_parent_node_name(ctx)
        parent = self._element_cache[parent_name]
        res = list(self._collect_joint_relations(ctx.joint_body(), parent))
        self._factory.connect_tuple_nodes(parent, name, res)
        return self.visitChildren(ctx)

    def visitInertia_body(self, ctx: CogniLangParser.Inertia_bodyContext):
        parent_name = self._generate_parent_name(ctx)
        if ctx.inertia_vector() is not None:
            v = self._extract_vector_field_values(ctx.inertia_vector().field_float_vector())
        __inertia = self._cognitive_element_factory.generate_semantic_element(
            'inertiaelement', f"inertia_{parent_name}", self._element_cache[parent_name],
            {'mass': float(ctx.mass.text)})
        return self.visitChildren(ctx)

    def visitAmbient(self, ctx: CogniLangParser.AmbientContext):
        name = extract_graphelement_signature(ctx.graphnode_signature())
        parent_name = self._generate_parent_node_name(ctx)
        parent_node = self._element_cache[parent_name]
        _el = self._factory.generate_node(name, parent_node)
        self._element_cache[_el.qualified_name] = _el
        # Create ambient graph definition and assign to hypergraph node
        self._cognitive_element_factory.generate_semantic_element(
            'ambientgraph', name, _el, {'name': name})
        return self.visitChildren(ctx)

    def __extract_exterior_sensor_type(self, ctx: CogniLangParser.Exteroceptive_sensorContext):
        return ctx.getText()

    def __extract_sensor_type(self, ctx: CogniLangParser.Sensor_typeContext):
        sensor_type = None
        if ctx.exteroceptive_sensor() is not None:
            sensor_type = "exterior"
            sensor_type = '/'.join([sensor_type, self.__extract_exterior_sensor_type(ctx.exteroceptive_sensor())])
        elif ctx.proprioceptive_sensor() is not None:
            sensor_type = "interior"
        return sensor_type

    def _get_basic_ambient_node_parameters(self, ctx):
        parent_name, parent_node = self._get_basic_node_parent_parameters(ctx)
        name = extract_graphelement_signature(ctx.ambient_element_signature())
        return parent_name, parent_node, name

    def visitSensor(self, ctx: CogniLangParser.SensorContext):
        parent_name, parent_node, name = self._get_basic_ambient_node_parameters(ctx)
        _el = self._factory.generate_node(name, parent_node)
        self._element_cache[_el.qualified_name] = _el
        sensor_type = self.__extract_sensor_type(ctx.sensor_type())
        _sv = self._cognitive_element_factory.generate_semantic_element(
            'sensorelement', name, _el, {'type': sensor_type})
        return self.visitChildren(ctx)

    def visitActuator(self, ctx: CogniLangParser.ActuatorContext):
        parent_name, parent_node, name = self._get_basic_ambient_node_parameters(ctx)
        _el = self._factory.generate_node(name, parent_node)
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)


    def visitPort(self, ctx:CogniLangParser.PortContext):
        parent_name, parent_node = self._get_basic_node_parent_parameters(ctx)
        name = extract_graphelement_signature(ctx.port_signature().graphnode_signature())
        _el = self._factory.generate_node(name, parent_node)
        self._element_cache[_el.qualified_name] = _el
        # Get topic name for port
        __topic_name = ctx.port_signature().topic_name.text
        __topic_msg = str(ctx.port_signature().msg.STRING())
        # Create port semantics
        _sv = self._cognitive_element_factory.generate_semantic_element(
            'ambienceport', name, _el, {'name': name, 'topicname': __topic_name, 'msgtype': __topic_msg}
        )
        return self.visitChildren(ctx)

    def visitSensor_placement(self, ctx: CogniLangParser.Sensor_placementContext):
        parent_name, parent_node, name = self._get_basic_edge_parameters(ctx)
        he = self._factory.create_hyperedge(parent_node, name)
        # Iterate sensor placements
        for pl in ctx.ambience_placement_element():
            if pl.element_placement_relation() is not None:
                __rel_placement = pl.element_placement_relation()
                __geom_relation: CogniLangParser.Geom_relationContext = __rel_placement.geom_relation()
                __dir: EnumRelationDirection = dir_enum_relation(__geom_relation.direction.text)
                __referenced_element_name: str = str(__geom_relation.referenced_element_.ID())
                __r = '/'.join([self.__root_entity.id_name, __referenced_element_name])
                __referenced_element = self._element_cache[__r]
                # Rigid transformation
                __placement_rel_name = '.'.join([name, __referenced_element_name])
                __placement: SensorPlacement = self._cognitive_element_factory.generate_semantic_element(
                    "sensorplacement", __placement_rel_name, he,
                    {'name': __placement_rel_name, 'reference': __referenced_element_name})
                __sv_trans = self._extract_rigid_transformation_element(__geom_relation, __placement)
                if __sv_trans is not None:
                    __placement.add_named_attribute('rigidtransformation', __sv_trans)
                #
                he.unary_connect(__referenced_element, 1.0, __dir, __placement)

    def visitAmbience_edge(self, ctx: CogniLangParser.Ambience_edgeContext):
        parent_name, parent_node, name = self._get_basic_edge_parameters(ctx)
        he = self._factory.create_hyperedge(parent_node, name)
        for __ae in ctx.ambience_edge_body():

            for comm in __ae.communication_connections():
                comm: CogniLangParser.Communication_connectionsContext
                __referenced_element = str(comm.ref_().ID())
                __ref_comm_element = self._element_cache['/'.join([parent_name, __referenced_element])]
                __dir: EnumRelationDirection = dir_enum_relation(comm.direction.text)
                if comm.comm_type.ambient_stream() is not None:
                    __communication_type = 'stream'
                elif comm.comm_type.ambient_signal() is not None:
                    __communication_type = 'signal'
                __sv_port_communication: AmbiencePortCommunication = \
                    self._cognitive_element_factory.generate_semantic_element(
                        'ambienceportcommunication', '/'.join(['comm', __referenced_element]), he,
                        {'type': __communication_type})
                he.unary_connect(__ref_comm_element, 1.0, __dir, __sv_port_communication)
        __sv = self._cognitive_element_factory.generate_semantic_element(
            'ambientnodeinterface', name, he, {'name': name})
        return self.visitChildren(ctx)
