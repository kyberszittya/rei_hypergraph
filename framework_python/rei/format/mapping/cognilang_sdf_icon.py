import asyncio

import typing
from lxml import etree

from rei.arbiter.cognitive_icon import CognitiveIcon
from rei.format.phys.inertia_context import encode_inertia_element
from rei.format.phys.kinematics.kinematic_semantic_context import encode_link_element, joint_base_element, \
    joint_base_element_endpoint
from rei.format.semantics.CognitiveEntity import KinematicJoint, KinematicLink, CognitiveEntity, \
    KinematicGraphDefinition
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge, HypergraphPort, HypergraphRelation
from rei.hypergraph.factorization_operations import RelationFactorization2SubsetOperation
from rei.query.query_engine import HierarchicalPrepositionQuery, HypergraphQueryEngine
from test.common.common_util import join_w_prefix_separator


class CognilangSdfIcon(CognitiveIcon):

    def __init__(self, clock):
        super().__init__()
        self.root_xml: etree.Element = etree.Element("sdf", attrib={"version": "1.7"})
        self.current_model = None
        self.cache = []
        self.__sub_engine = HypergraphQueryEngine("engine", b'00', "engine/engine", clock, None)

    def __add_model_element(self, element):
        # Wrap-up
        if self.current_model is None:
            self.cache.append(element)
        else:
            self.current_model.append(element)

    def encode_element(self, element, prefix=""):
        match element:
            case KinematicLink():
                link_el = encode_link_element(element, prefix)
                # Add link to current model
                self.__add_model_element(link_el)
                # Try to process inertia as well
                for iner in encode_inertia_element(element):
                    link_el.append(iner)
            case CognitiveEntity():
                element: CognitiveEntity
                model_el = etree.Element("model")
                model_el.attrib["name"] = element.id_name
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

    @staticmethod
    def __is_kinematic_graph(el: HypergraphNode):
        return len(list(el.get_subelements(lambda x: isinstance(x, KinematicGraphDefinition)))) > 0

    async def get_canonical_link(self, graph: HypergraphNode) -> typing.Set:
        __sub_engine = HypergraphQueryEngine("engine", b'00', "engine/engine", self.__sub_engine.clock, None)
        __sub_engine.clear()
        link_query = HierarchicalPrepositionQuery(
            graph, lambda x: isinstance(x, KinematicLink), lambda x: True)
        joint_query = HierarchicalPrepositionQuery(graph, lambda x: isinstance(x, KinematicJoint), lambda x: True)
        __sub_engine.add_query(f'{graph.id_name}_link_query', link_query)
        __sub_engine.add_query(f'{graph.id_name}_joint_query', joint_query)
        res = await __sub_engine.execute()
        links = set(filter(lambda x: isinstance(x, KinematicLink), res))
        joints = filter(lambda x: isinstance(x, KinematicJoint), res)
        for j in joints:
            e: HypergraphEdge = j.parent.parent
            #links = links.difference([x.endpoint for x in e.get_incoming_relations()])
            for x in e.get_outgoing_relations():
                links = links.difference(set(x.endpoint.get_subelements(lambda x: isinstance(x, KinematicLink))))

        return links


    async def encode_sub_graph(self, joint, prefix):
        self.__sub_engine.clear()
        prefix_t1 = prefix + joint.parent.id_name
        link_query = HierarchicalPrepositionQuery(
            joint.endpoint, lambda x: isinstance(x, KinematicLink), lambda x: True)
        joint_query = HierarchicalPrepositionQuery(
            joint.endpoint, lambda x: isinstance(x, KinematicJoint), lambda x: True)
        self.__sub_engine.add_query(f'{joint.id_name}_link_query', link_query)
        self.__sub_engine.add_query(f'{joint.id_name}_joint_query', joint_query)
        res = await self.__sub_engine.execute()
        await self.encode(res, prefix_t1)

    async def encode(self, elements, prefix=""):
        cognitive_entities = filter(lambda x: isinstance(x, CognitiveEntity), elements)
        # Cognitive elements
        for i in cognitive_entities:
            self.encode_element(i)
        # Nodes
        links = filter(lambda x: isinstance(x, KinematicLink), elements)
        for i in links:
            self.encode_element(i, prefix)
        # Joint subset factorization
        __selected_elements = [x.parent for x in filter(lambda x: isinstance(x, KinematicLink), elements)]
        __selected_elements.extend([x.parent for x in filter(lambda x0: isinstance(x0, KinematicJoint), elements)])
        # Query
        query = RelationFactorization2SubsetOperation()
        joints = await query.execute(__selected_elements)
        for j0, j1 in joints:
            j0: HypergraphRelation
            j1: HypergraphRelation
            if not CognilangSdfIcon.__is_kinematic_graph(j1.endpoint):
                joint_el = joint_base_element(j0, j1, prefix)
                self.__add_model_element(joint_el)
            else:
                __canonical_link = (await self.get_canonical_link(j1.endpoint)).pop()
                #print(__canonical_link.id_name)
                __joint = next(j1.get_subelements(lambda x: isinstance(x, KinematicJoint)))
                joint_el = joint_base_element_endpoint(
                    j0, j1, join_w_prefix_separator([j1.parent.id_name, "connect", __canonical_link.id_name], '.', prefix),
                    f"{j1.parent.id_name}.{__canonical_link.id_name}", prefix)
                self.__add_model_element(joint_el)
                await self.encode_sub_graph(j1, prefix)



