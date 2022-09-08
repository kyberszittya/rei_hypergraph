import math
import typing

from rei.factories.foundation_factory import HypergraphFactory
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.cognilang.CogniLangVisitor import CogniLangVisitor
from rei.format.mapping.cognilang_mapping_errors import ErrorParserNoFactorySet
from rei.format.mapping.cognilang_map_utility import dir_enum_relation, extract_graphelement_signature
from rei.format.semantics.cognitive_entity_semantic_factory import CognitiveEntitySemanticFactory
from rei.foundations.clock import MetaClock
from rei.hypergraph.base_elements import HypergraphNode, HypergraphElement
from rei.hypergraph.common_definitions import EnumRelationDirection


__DEFAULT_ROTATION_LIST = [0.0, 0.0, 0.0]


class CognilangParserFileIcon(CogniLangVisitor):

    def __init__(self, icon_name: str, clock: MetaClock):
        super().__init__()
        self._element_cache = {}
        self.__icon_name = icon_name
        self.__clock = clock
        self.__factory = HypergraphFactory(f"factory_{self.__icon_name}", self.__clock)
        self.__cognitive_element_factory = CognitiveEntitySemanticFactory(f"cogni_{self.__icon_name}", self.__clock)
        self.__root_entity = None
        # Handling special world node
        self._element_cache['world'] = self.__factory.generate_node("world", None)
        # Reference cache
        self._reference_cache: dict[str, HypergraphElement] = dict[str, HypergraphElement]()

    @property
    def root_entity(self):
        return self.__root_entity

    #
    # SECTION: utility functions
    #

    def __get_parent_name(self, ctx):
        if hasattr(ctx, 'ID'):
            yield str(ctx.ID())
        elif hasattr(ctx, 'graphnode_signature'):
            yield extract_graphelement_signature(ctx.graphnode_signature())
        elif hasattr(ctx, 'graphedge_signature'):
            yield extract_graphelement_signature(ctx.graphedge_signature())
        if ctx.parentCtx is not None:
            yield from self.__get_parent_name(ctx.parentCtx)

    def __generate_parent_name(self, ctx):
        return '/'.join(list(self.__get_parent_name(ctx))[::-1][:-1])

    def __lookup_reference(self, ctx, parent):
        if hasattr(ctx, "ref_"):
            reference_name = str(ctx.ref_().ID())
            # Special joint fixed to world
            if reference_name == "world":
                return self._element_cache["world"], reference_name
            else:
                return list(parent.get_element_by_id_name(reference_name))[0], reference_name

    def __extract_joint_relation(self, ctx: CogniLangParser.Joint_relationContext, parent: HypergraphElement):
        __endpoint, reference_name = self.__lookup_reference(ctx, parent)
        __direction = dir_enum_relation(ctx.direction.text)
        # Joint attributes
        __joint_type: str = str(ctx.type_)
        __joint_edge_name = extract_graphelement_signature(ctx.parentCtx.parentCtx.graphedge_signature())

        # Semantic value setup
        __semantic_value_node = self.__cognitive_element_factory.generate_semantic_element(
            "kinematicjoint", f"joint_{__joint_edge_name}.{reference_name}", parent, {
                "joint_type": __joint_type
            })
        # Extract rigid transformation
        values = None
        if ctx.rigid_transformation() is not None:
            _translation, _rotation, _rotation_type = self.__extract_rigid_transformation(ctx.rigid_transformation())
            _sv_trans = self.__cognitive_element_factory.generate_semantic_element(
                'rigidtransformation', f"joint.{parent.id_name}_{reference_name}.transformation", __semantic_value_node,
                {'translation': _translation, 'rotation': _rotation, 'rotation_type': _rotation_type})
            __semantic_value_node.add_named_attribute('rigid_transformation', _sv_trans)
            # Set rigid transformation as a value
            match _rotation_type:
                case 'deg':
                    _rotation = [float(x)*math.pi/180.0 for x in _rotation]
                case _:
                    _rotation = [float(x) for x in _rotation]
            values = [_translation, _rotation]
        # Extract rigid transformation
        return __endpoint, __direction, values, __semantic_value_node

    def __collect_joint_relations(self, ctx: CogniLangParser.Joint_bodyContext, parent: HypergraphElement):
        for rel in ctx.joint_relation():
            yield self.__extract_joint_relation(rel, parent)

    def __get_lookup_name_depth(self, ctx, min_depth: int, current_depth: int = 0):
        depth = current_depth
        if hasattr(ctx, 'ID'):
            if min_depth <= current_depth:
                yield str(ctx.ID())
            depth += 1
        elif hasattr(ctx, 'graphnode_signature'):
            if min_depth <= current_depth:
                yield extract_graphelement_signature(ctx.graphnode_signature())
            depth += 1
        elif hasattr(ctx, 'graphedge_signature'):
            yield extract_graphelement_signature(ctx.graphedge_signature())
        if ctx.parentCtx is not None:
            yield from self.__get_lookup_name_depth(ctx.parentCtx, min_depth, depth)

    def __lookup_name(self, ctx, depth: int = 0):
        return list(self.__get_lookup_name_depth(ctx, depth))[::-1]

    def __lookup_node_container(self, ctx, node_filter: typing.Callable[[typing.Any], bool]):
        _names = list(self.__get_parent_name(ctx))[::-1][:-1]
        for i in range(len(_names)):
            _name = '/'.join(_names[:-i])
            if _name in self._element_cache:
                if node_filter(self._element_cache[_name]):
                    return self._element_cache[_name]
        return None

    def __search_for_reference(self, reference, parent_ctx):
        reference_name: str = str(reference.ID())
        tags = reference_name.split('/')
        depth = len(tags)
        inferred_name = '/'.join([*self.__lookup_name(parent_ctx, depth), *tags])
        if inferred_name in self._element_cache:
            return self._element_cache[inferred_name], inferred_name
        return None

    def __add_geometry_reference(self, ctx, container_node):
        parent_graph_name = '/'.join(list(self.__get_parent_name(ctx))[::-1][:-2])
        parent_graph: HypergraphNode = self._element_cache[parent_graph_name]
        _el_ref, _inferred_name = self.__search_for_reference(ctx.geometries().ref_(), ctx)
        if _inferred_name not in self._reference_cache:
            ref_e = self.__factory.create_hyperedge(
                parent_graph, f"ref_{container_node.id_name}_{str(ctx.geometries().ref_().ID())}")
            ref_e.unary_connect(_el_ref, None, EnumRelationDirection.OUTWARDS)
            ref_e.unary_connect(container_node, None, EnumRelationDirection.INWARDS)
            self._reference_cache[_inferred_name] = ref_e

    def __add_reference(self, ctx, container_node):
        parent_graph_name = '/'.join(list(self.__get_parent_name(ctx))[::-1][:-2])
        parent_graph: HypergraphNode = self._element_cache[parent_graph_name]
        _el_ref, _inferred_name = self.__search_for_reference(ctx.ref_(), ctx)
        if _inferred_name not in self._reference_cache:
            ref_e = self.__factory.create_hyperedge(
                parent_graph, f"ref_{container_node.id_name}_{str(ctx.ref_().ID())}")
            ref_e.unary_connect(_el_ref, None, EnumRelationDirection.OUTWARDS)
            ref_e.unary_connect(container_node, None, EnumRelationDirection.INWARDS)
            self._reference_cache[_inferred_name] = ref_e

    def __extract_vector_field_values(self, ctx: CogniLangParser.Field_float_vectorContext):
        yield from self.__extract_float_vector_values(ctx.float_vector())

    def __extract_float_vector_values(self, ctx: CogniLangParser.Float_vectorContext, parent=None):
        for x in ctx.value():
            if x.ref_() is not None:
                yield self.__factory.create_value(parent, '_'.join([parent.id_name, x.ref().ID()]))
            else:
                yield float(str(x.FLOAT()))

    def __collect_geometries(self, ctx: CogniLangParser.Geometry_bodyContext, container_node: HypergraphNode):
        if ctx.geometries().ref_() is not None:
            self.__add_geometry_reference(ctx, container_node)
        else:
            __geom_id_name = '_'.join(["geom", container_node.id_name])
            _el = self.__factory.generate_node(__geom_id_name, container_node)
            geom_ctx: typing.Any = None
            __geometry_type: str = ""
            if ctx.geometries().cylinder_geometry() is not None:
                geom_ctx: CogniLangParser.Cylinder_geometryContext = ctx.geometries().cylinder_geometry()
                __geometry_type = 'cylindergeometry'
            elif ctx.geometries().polyhedron_geometry() is not None:
                geom_ctx: CogniLangParser.Polyhedron_geometryContext = ctx.geometries().polyhedron_geometry()
                __geometry_type = 'polyhedrongeometry'
            elif ctx.geometries().ellipsoid_geometry() is not None:
                geom_ctx: CogniLangParser.Ellipsoid_geometryContext = ctx.geometries().ellipsoid_geometry()
                __geometry_type = 'ellipsoidgeometry'
            elif ctx.geometries().mesh_geometry() is not None:
                geom_ctx: CogniLangParser.Mesh_geometryContext = ctx.geometries().mesh_geometry()
                __geometry_type = 'meshgeometry'
            if geom_ctx is not None:
                values = list(self.__extract_vector_field_values(geom_ctx.field_float_vector()))
                _sv = self.__cognitive_element_factory.generate_semantic_element(
                    __geometry_type, __geom_id_name, _el, {'name': __geom_id_name}, values)
                self._element_cache[_sv.qualified_name] = _sv
            # Wrap up
            self._element_cache[_el.qualified_name] = _el

    def __collect_materials(self, ctx: CogniLangParser.MaterialContext, container_node: HypergraphNode):
        __material_name_id = f'material_{container_node.id_name}'
        _sv = self.__cognitive_element_factory.generate_semantic_element(
            'material', __material_name_id, container_node,
            {'name': __material_name_id, 'material_name': ctx.material_name})
        self._element_cache[_sv.qualified_name] = _sv

    def __extract_rigid_transformation(self, ctx: CogniLangParser.Rigid_transformationContext):
        translation = list(self.__extract_float_vector_values(ctx.float_vector()))
        if ctx.rotation() is not None:
            rotation = list(self.__extract_float_vector_values(ctx.rotation().float_vector()))
            rotation_type = str(ctx.rotation().rot_type)
            return translation, rotation, rotation_type
        rotation = [0.0, 0.0, 0.0]
        rotation_type = 'deg'
        return translation, rotation, rotation_type

    def __extract_rigid_transformation_element(self, ctx, _el):
        if ctx.rigid_transformation() is not None:
            _translation, _rotation, _rotation_type = self.__extract_rigid_transformation(ctx.rigid_transformation())
            trans_id_container: str = '_'.join([_el.id_name, 'transformation'])
            _sv_trans = self.__cognitive_element_factory.generate_semantic_element(
                'rigidtransformation', trans_id_container, _el,
                {'translation': _translation, 'rotation': _rotation, 'rotation_type': _rotation_type})
            self._element_cache[_sv_trans.qualified_name] = _sv_trans
            return _sv_trans

    #
    # END SECTION
    #

    #
    # SECTION: visitor overrides
    #

    def visitRootnode(self, ctx: CogniLangParser.RootnodeContext):
        if self.__factory is None:
            raise ErrorParserNoFactorySet
        return self.visitChildren(ctx)

    def visitEntity(self, ctx: CogniLangParser.EntityContext):
        name = str(ctx.graphnode_signature().ID())
        # Create entity as hypergraph
        _n = self.__factory.generate_node(name, None)
        self.__root_entity = _n
        self.__cognitive_element_factory.generate_semantic_element('cognitiveentity', name, self.__root_entity,
                                                                   {'name': name})
        self._element_cache[_n.qualified_name] = _n
        # Return to context
        return self.visitChildren(ctx)

    def visitKinematic(self, ctx: CogniLangParser.KinematicContext):
        name = extract_graphelement_signature(ctx.graphnode_signature())
        _el = self.__factory.generate_node(name, self.__root_entity)
        self.__cognitive_element_factory.generate_semantic_element('kinematicgraph', name, _el,
                                                                   {'name': name})
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)

    def visitVisual_node(self, ctx: CogniLangParser.Visual_nodeContext):
        _parent = self.__generate_parent_name(ctx)
        _name = str(ctx.ID())
        # Create node
        _el = self.__factory.generate_node(_name, self._element_cache[_parent])
        self._element_cache[_el.qualified_name] = _el
        # Extract geometry elements
        self.__collect_geometries(ctx.geometry_body(), _el)
        self.__collect_materials(ctx.material(), _el)
        return self.visitChildren(ctx)

    def visitCollision_node(self, ctx: CogniLangParser.Collision_nodeContext):
        _parent = self.__generate_parent_name(ctx)
        _name = str(ctx.ID())
        # Create node
        _el = self.__factory.generate_node(_name, self._element_cache[_parent])
        self._element_cache[_el.qualified_name] = _el
        # Extract geometry elements
        self.__collect_geometries(ctx.geometry_body(), _el)
        return self.visitChildren(ctx)

    def visitLink(self, ctx: CogniLangParser.LinkContext):
        name = extract_graphelement_signature(ctx.graphnode_signature())
        parent_name = self.__generate_parent_name(ctx)
        parent = self._element_cache[parent_name]
        _el = self.__factory.generate_node(name, parent)
        #
        self.__extract_rigid_transformation_element(ctx, _el)
        #
        self.__cognitive_element_factory.generate_semantic_element('kinematiclink', name, _el,
                                                                   {'name': name})
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)

    def visitJoint(self, ctx: CogniLangParser.JointContext):
        name = extract_graphelement_signature(ctx.graphedge_signature())
        parent_name = self.__generate_parent_name(ctx)
        parent = self._element_cache[parent_name]
        res = list(self.__collect_joint_relations(ctx.joint_body(), parent))
        self.__factory.connect_tuple_nodes(parent, name, res)
        return self.visitChildren(ctx)
