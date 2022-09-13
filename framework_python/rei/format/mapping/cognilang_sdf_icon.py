from lxml import etree

from rei.arbiter.cognitive_icon import CognitiveIcon
from rei.format.phys.inertia_context import encode_inertia_element
from rei.format.phys.kinematics.kinematic_semantic_context import encode_link_element, joint_base_element
from rei.format.semantics.CognitiveEntity import KinematicJoint, KinematicLink, CognitiveEntity
from rei.hypergraph.factorization_operations import RelationFactorization2SubsetOperation


class CognilangSdfIcon(CognitiveIcon):

    def __init__(self):
        super().__init__()
        self.root_xml: etree.Element = etree.Element("sdf", attrib={"version":"1.7"})
        self.current_model = None
        self.cache = []

    def __add_model_element(self, element):
        # Wrap-up
        if self.current_model is None:
            self.cache.append(element)
        else:
            self.current_model.append(element)

    def encode_element(self, element):
        match element:
            case KinematicLink():
                link_el = encode_link_element(element)
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
            joint_el = joint_base_element(j[0], j[1])
            self.__add_model_element(joint_el)
