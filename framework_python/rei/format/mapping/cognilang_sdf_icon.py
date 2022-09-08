import lxml
from lxml import etree

from rei.format.semantics.CognitiveEntity import KinematicJoint, KinematicLink, CognitiveEntity


class CognilangSdfIcon(object):

    def __init__(self):
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
                element: KinematicLink
                link_el = etree.Element("link")
                self.__add_model_element(link_el)
            case CognitiveEntity():
                element: CognitiveEntity
                model_el = etree.Element("model")
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

