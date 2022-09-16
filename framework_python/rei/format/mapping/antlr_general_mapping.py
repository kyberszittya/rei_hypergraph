import typing

from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.factories.foundation_factory import HypergraphFactory
from rei.format.mapping.cognilang_map_utility import extract_graphelement_signature
from rei.format.semantics.cognitive_entity_semantic_factory import CognitiveEntitySemanticFactory
from rei.hypergraph.base_elements import HypergraphNode, HypergraphElement
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.value_node import ValueNode


class GeneralGraphMapping(object):

    def __init__(self,  icon_name, clock) -> None:
        super().__init__()
        self._element_cache = {}
        self._icon_name = icon_name
        self._clock = clock
        self._factory = HypergraphFactory(f"factory_{self._icon_name}", self._clock)
        # Reference cache
        self._reference_cache: dict[str, HypergraphElement] = dict[str, HypergraphElement]()
        # Cognitive element factory
        self._cognitive_element_factory = CognitiveEntitySemanticFactory(f"cogni_{self._icon_name}", self._clock)
        # Create parameter hypergraph
        self._parameters = self._factory.generate_node("parameters")
        # Element wildcards
        self._element_reference_wildcards = set()

    def _get_parent_name(self, ctx):
        if hasattr(ctx, 'ID'):
            yield str(ctx.ID())
        elif hasattr(ctx, 'graphnode_signature'):
            yield extract_graphelement_signature(ctx.graphnode_signature())
        elif hasattr(ctx, 'graphedge_signature'):
            yield extract_graphelement_signature(ctx.graphedge_signature())
        if ctx.parentCtx is not None:
            yield from self._get_parent_name(ctx.parentCtx)

    def _get_lookup_name_depth(self, ctx, min_depth: int, current_depth: int = 0):
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
            yield from self._get_lookup_name_depth(ctx.parentCtx, min_depth, depth)

    def _lookup_name(self, ctx, depth: int = 0):
        return list(self._get_lookup_name_depth(ctx, depth))[::-1]

    def _search_for_reference(self, reference, parent_ctx):
        reference_name: str = str(reference.ID())
        tags = reference_name.split('/')
        depth = len(tags)
        inferred_name = '/'.join([*self._lookup_name(parent_ctx, depth), *tags])
        if inferred_name in self._element_cache:
            return self._element_cache[inferred_name], inferred_name
        return None

    def _lookup_node_container(self, ctx, node_filter: typing.Callable[[typing.Any], bool]):
        _names = list(self._get_parent_name(ctx))[::-1][:-1]
        for i in range(len(_names)):
            _name = '/'.join(_names[:-i])
            if _name in self._element_cache:
                if node_filter(self._element_cache[_name]):
                    return self._element_cache[_name]
        return None

    def _get_basic_node_parent_parameters(self, ctx):
        parent_name = self._generate_parent_name(ctx)
        parent_node = self._element_cache[parent_name]
        return parent_name, parent_node

    def _generate_parent_node_name(self, ctx):
        return '/'.join(list(self._get_parent_name(ctx))[::-1][:-1])

    def _generate_parent_name(self, ctx):
        return '/'.join(list(self._get_parent_name(ctx))[::-1])

    def _lookup_reference(self, ctx, parent):
        if hasattr(ctx, "ref_"):
            reference_name = str(ctx.ref_().ID())
            # Special joint fixed to world
            if reference_name in self._element_reference_wildcards:
                return self._element_cache[reference_name], reference_name
            else:
                return list(parent.get_element_by_id_name(reference_name))[0], reference_name

    def _add_reference(self, ctx, container_node, ref_func: typing.Callable):
        parent_graph_name = '/'.join(list(self._get_parent_name(ctx))[::-1][:-2])
        parent_graph: HypergraphNode = self._element_cache[parent_graph_name]
        _el_ref, _inferred_name = self._search_for_reference(ref_func(ctx).ref_(), ctx)
        if _inferred_name not in self._reference_cache:
            ref_e = self._factory.create_hyperedge(
                parent_graph, f"ref_{container_node.id_name}_{str(ref_func(ctx).ref_().ID())}")
            ref_e.unary_connect(_el_ref, None, EnumRelationDirection.OUTWARDS)
            ref_e.unary_connect(container_node, None, EnumRelationDirection.INWARDS)
            self._reference_cache[_inferred_name] = ref_e

    def _extract_vector_field_values(self, ctx: CogniLangParser.Field_float_vectorContext):
        yield from self._extract_float_vector_values(ctx.float_vector())

    def _extract_float_vector_values(self, ctx: CogniLangParser.Float_vectorContext, parent=None):
        for x in ctx.value():
            if x.ref_() is not None:
                __ref_name = str(x.ref_().ID())
                p = next(self._parameters.get_subelements(
                    lambda v: isinstance(v, ValueNode) and v.id_name == __ref_name))
                for _p in p.get_values():
                    yield float(_p)
            else:
                yield float(str(x.FLOAT()))
