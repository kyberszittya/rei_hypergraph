from rei.factories.foundation_factory import HypergraphFactory
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.cognilang.CogniLangVisitor import CogniLangVisitor
from rei.format.semantics.CognitiveEntity import CognitiveEntity, KinematicJoint
from rei.format.semantics.CognitiveEntitySemanticFactory import CognitiveEntitySemanticFactory
from rei.foundations.clock import MetaClock
from rei.hypergraph.base_elements import HypergraphNode, HypergraphElement, HypergraphRelation
from rei.hypergraph.common_definitions import EnumRelationDirection


class ErrorParserNoFactorySet(Exception):
    pass


class ErrorInvalidDirection(Exception):
    pass


class CognilangParserFileIcon(CogniLangVisitor):

    def __init__(self, icon_name: str, clock: MetaClock):
        super().__init__()
        self._element_cache = {}
        self.__icon_name = icon_name
        self.__clock = clock
        self.__factory = HypergraphFactory(f"factory_{self.__icon_name}", self.__clock)
        self.__cognitive_element_factory = CognitiveEntitySemanticFactory(f"cogni_{self.__icon_name}", self.__clock)
        self.__root_entity = None
        # TODO: handle world
        self._element_cache['world'] = self.__factory.generate_node("world", None)

    @property
    def root_entity(self):
        return self.__root_entity


    #
    # SECTION: utility functions
    #

    def __extract_graphelement_signature(self, ctx: CogniLangParser.Graphnode_signatureContext):
        return str(ctx.ID())

    def __extract_linknodebody(self, ctx: CogniLangParser.Linknode_bodyContext) -> list[HypergraphNode]:
        return

    def __get_parent_name(self, ctx):
        if hasattr(ctx, 'ID'):
            yield str(ctx.ID())
        elif hasattr(ctx, 'graphnode_signature'):
            yield self.__extract_graphelement_signature(ctx.graphnode_signature())
        elif hasattr(ctx, 'graphedge_signature'):
            yield self.__extract_graphelement_signature(ctx.graphedge_signature())
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

    def __dir_enum_relation(self, dir: str):
        match dir:
            case '<-':
                return EnumRelationDirection.INWARDS
            case '->':
                return EnumRelationDirection.OUTWARDS
            case '--':
                return EnumRelationDirection.BIDIRECTIONAL
        raise ErrorInvalidDirection

    def __extract_joint_relation(self, ctx: CogniLangParser.Joint_relationContext, parent: HypergraphElement):
        __endpoint, reference_name = self.__lookup_reference(ctx, parent)
        __direction = self.__dir_enum_relation(ctx.direction.text)
        # Joint attributes
        __joint_type: str = str(ctx.type_)
        # Semantic value setup
        __semantic_value_node = self.__cognitive_element_factory.generate_semantic_element(
            "kinematicjoint", f"joint.{parent.id_name}_{reference_name}", parent, {
                "joint_type": __joint_type
            })
        return __endpoint, __direction, None, __semantic_value_node

    def __collect_joint_relations(self, ctx: CogniLangParser.Joint_bodyContext, parent: HypergraphElement):
        for rel in ctx.joint_relation():
            yield self.__extract_joint_relation(rel, parent)

    def __collect_geometries(self, ctx: CogniLangParser.Geometry_bodyContext):
        if ctx.geometries().ref_() is not None:
            print(ctx.geometries().ref_().ID())



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

    def visitKinematic(self, ctx:CogniLangParser.KinematicContext):
        name = self.__extract_graphelement_signature(ctx.graphnode_signature())
        _el = self.__factory.generate_node(name, self.__root_entity)
        self.__cognitive_element_factory.generate_semantic_element('kinematicgraph', name, _el,
                                                                   {'name': name})
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)

    def visitVisual_node(self, ctx: CogniLangParser.Visual_nodeContext):
        _parent = self.__generate_parent_name(ctx)
        _name = str(ctx.ID())
        # Extract geometry elements
        self.__collect_geometries(ctx.geometry_body())
        # Create node
        _el = self.__factory.generate_node(_name, self._element_cache[_parent])
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)

    def visitCollision_node(self, ctx: CogniLangParser.Collision_nodeContext):
        _parent = self.__generate_parent_name(ctx)
        _name = str(ctx.ID())
        # Extract geometry elements
        self.__collect_geometries(ctx.geometry_body())
        # Create node
        _el = self.__factory.generate_node(_name, self._element_cache[_parent])
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)

    def visitLink(self, ctx: CogniLangParser.LinkContext):
        name = self.__extract_graphelement_signature(ctx.graphnode_signature())
        parent_name = self.__generate_parent_name(ctx)
        parent = self._element_cache[parent_name]
        _el = self.__factory.generate_node(name, parent)
        self.__cognitive_element_factory.generate_semantic_element('kinematiclink', name, _el,
                                                                   {'name': name})
        self._element_cache[_el.qualified_name] = _el
        return self.visitChildren(ctx)

    def visitJoint(self, ctx: CogniLangParser.JointContext):
        name = self.__extract_graphelement_signature(ctx.graphedge_signature())
        parent_name = self.__generate_parent_name(ctx)
        parent = self._element_cache[parent_name]
        res = list(self.__collect_joint_relations(ctx.joint_body(), parent))
        he = self.__factory.connect_tuple_nodes(parent, name, res)
        return self.visitChildren(ctx)
