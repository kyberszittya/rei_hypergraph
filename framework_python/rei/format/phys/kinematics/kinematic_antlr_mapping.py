import typing

from rei.format.mapping.antlr_general_mapping import GeneralGraphMapping
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.mapping.cognilang_map_utility import dir_enum_relation, extract_graphelement_signature
from rei.format.phys.kinematics.kinematic_semantic_context import generate_joint_name
from rei.hypergraph.base_elements import HypergraphElement, HypergraphNode

import math


class KinematicGraphContextMapper(GeneralGraphMapping):

    __SPECIAL_FIXED_WORLD_FRAME = 'world'

    def __init__(self, icon_name, clock):
        super().__init__(icon_name, clock)
        # Handling special world kinematic node
        self._element_cache[KinematicGraphContextMapper.__SPECIAL_FIXED_WORLD_FRAME] = \
            self._factory.generate_node(KinematicGraphContextMapper.__SPECIAL_FIXED_WORLD_FRAME, None)
        self._element_reference_wildcards.add(KinematicGraphContextMapper.__SPECIAL_FIXED_WORLD_FRAME)



    def _get_basic_edge_parameters(self, ctx):
        parent_name = self._generate_parent_node_name(ctx)
        parent_node = self._element_cache[parent_name]
        name = extract_graphelement_signature(ctx.graphedge_signature())
        return parent_name, parent_node, name

    def _collect_joint_relations(self, ctx: CogniLangParser.Joint_bodyContext, parent: HypergraphElement):
        for rel in ctx.joint_relation():
            yield self._extract_joint_relation(rel, parent)

    def _extract_joint_relation(self, ctx: CogniLangParser.Joint_relationContext, parent: HypergraphElement):
        __endpoint, reference_name = self._lookup_reference(ctx, parent)
        __direction = dir_enum_relation(ctx.direction.text)
        # Joint attributes
        __joint_type: str = str(ctx.type_.value_.text)
        __joint_edge_name = extract_graphelement_signature(ctx.parentCtx.parentCtx.graphedge_signature())
        # Semantic value setup
        __joint_name = generate_joint_name(__joint_edge_name, reference_name)
        __semantic_value_node = self._cognitive_element_factory.generate_semantic_element(
            "kinematicjoint", __joint_name, parent, {
                "joint_type": __joint_type
            })
        # Extract rigid transformation
        values = None
        if ctx.axis() is not None:
            __ax = self._extract_float_vector_values(ctx.axis().axis_)
            __semantic_value_node.add_named_attribute('axis', [float(x) for x in __ax])
        if ctx.rigid_transformation() is not None:
            _sv_trans, _translation, _rotation = self._extract_rigid_transformation_element(ctx, __semantic_value_node)
            # Set rigid transformation as a value
            values = [_translation, _rotation]
        # Extract rigid transformation
        return __endpoint, __direction, values, __semantic_value_node

    def _extract_rigid_transformation_element(self, ctx, _el):
        if ctx.rigid_transformation() is not None:
            _translation, _rotation, _rotation_type = self._extract_rigid_transformation(ctx.rigid_transformation())
            trans_id_container: str = '_'.join([_el.id_name, 'transformation'])
            _sv_trans = self._cognitive_element_factory.generate_semantic_element(
                'rigidtransformation', trans_id_container, _el,
                {'translation': _translation, 'rotation': _rotation, 'rotation_type': _rotation_type})
            match _rotation_type:
                case 'deg':
                    _rotation = [float(x)*math.pi/180.0 for x in _rotation]
                case _:
                    _rotation = [float(x) for x in _rotation]
            self._element_cache[_sv_trans.qualified_name] = _sv_trans
            return _sv_trans, _translation, _rotation

    def _extract_rigid_transformation(self, ctx: CogniLangParser.Rigid_transformationContext):
        translation = list(self._extract_float_vector_values(ctx.float_vector()))
        if ctx.rotation() is not None:
            rotation = list(self._extract_float_vector_values(ctx.rotation().float_vector()))
            rotation_type = 'rad'
            if ctx.rotation().rot_type is not None:
                rotation_type = str(ctx.rotation().rot_type.text)
                if 'd' == rotation_type[0]:
                    rotation_type = 'deg'
            return translation, rotation, rotation_type
        else:
            rotation = [0.0, 0.0, 0.0]
            rotation_type = 'deg'
            return translation, rotation, rotation_type

    #
    # SECTION: utility functions
    #

    def _collect_geometries(self, ctx: CogniLangParser.Geometry_bodyContext, container_node: HypergraphNode):
        __geom_id_name = '_'.join(["geom", container_node.id_name])
        _el = self._factory.generate_node(__geom_id_name, container_node)
        if ctx.geometries().ref_() is not None:
            self._add_reference(ctx, _el, lambda x: x.geometries())
        else:
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
                values = list(self._extract_vector_field_values(geom_ctx.field_float_vector()))
                _sv = self._cognitive_element_factory.generate_semantic_element(
                    __geometry_type, __geom_id_name, _el, {'name': __geom_id_name}, values)
                self._element_cache[_sv.qualified_name] = _sv
        # Wrap up
        self._element_cache[_el.qualified_name] = _el

    def _collect_materials(self, ctx: CogniLangParser.MaterialContext, container_node: HypergraphNode):
        __material_name_id = f'material_{container_node.id_name}'
        mat_name = 'white'
        if ctx is not None:
            if ctx.material_name is not None:
                mat_name = ctx.material_name.text
        _sv = self._cognitive_element_factory.generate_semantic_element(
            'material', __material_name_id, container_node,
            {'name': __material_name_id, 'material_name': mat_name})
        self._element_cache[_sv.qualified_name] = _sv

    #
    # END SECTION
    #