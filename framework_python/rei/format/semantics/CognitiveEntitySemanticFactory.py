import typing

from rei.factories.abstract_factory import AbstractElementFactory, ErrorInsufficientValues
from rei.format.semantics.CognitiveEntity import CognitiveEntity, KinematicGraphDefinition, KinematicLink, \
    KinematicJoint
from rei.foundations.clock import MetaClock


class CognitiveEntitySemanticFactory(AbstractElementFactory):

    def __init__(self, factory_name: str, clock: MetaClock):
        super().__init__(factory_name, clock)

    def generate_semantic_element(self, raw_element_type: str, id_name, parent, attr: dict[str, typing.Any]):
        if len(attr)==0:
            raise ErrorInsufficientValues
        element_type = ''.join(raw_element_type.lower().strip().split('_'))
        match element_type:
            case 'cognitiveentity':
                return CognitiveEntity(self.unique_identifier.generate_uid(id_name), id_name,
                                       self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematicgraph':
                return KinematicGraphDefinition(self.unique_identifier.generate_uid(id_name), id_name,
                                                self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematiclink':
                return KinematicLink(self.unique_identifier.generate_uid(id_name), id_name,
                                     self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematicjoint':
                return KinematicJoint(self.unique_identifier.generate_uid(id_name), id_name,
                                      self.get_stamped_qualified_name(id_name, parent), parent, attr)
