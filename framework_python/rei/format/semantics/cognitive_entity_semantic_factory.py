import typing

from rei.factories.abstract_factory import AbstractElementFactory, ErrorInsufficientValues
from rei.format.semantics.CognitiveEntity import CognitiveEntity, KinematicGraphDefinition, KinematicLink, \
    KinematicJoint, CylinderGeometry, PolyhedronGeometry, EllipsoidGeometry, VisualMaterial, RigidTransformation
from rei.foundations.clock import MetaClock


class InvalidSemanticType(Exception):
    pass


class CognitiveEntitySemanticFactory(AbstractElementFactory):

    def __init__(self, factory_name: str, clock: MetaClock):
        super().__init__(factory_name, clock)

    def generate_semantic_element(self, raw_element_type: str, id_name, parent, attr: dict[str, typing.Any], values=None):
        if len(attr)==0:
            raise ErrorInsufficientValues
        element_type = ''.join(raw_element_type.lower().strip().split('_'))
        uuid = self.unique_identifier.generate_uid(id_name)
        match element_type:
            case 'cognitiveentity':
                return CognitiveEntity(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematicgraph':
                return KinematicGraphDefinition(uuid, id_name,
                                                self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematiclink':
                return KinematicLink(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematicjoint':
                return KinematicJoint(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'cylindergeometry':
                return CylinderGeometry(uuid, id_name, self.get_stamped_qualified_name(id_name, parent),
                                        parent, attr, values)
            case 'polyhedrongeometry':
                return PolyhedronGeometry(uuid, id_name, self.get_stamped_qualified_name(id_name, parent),
                                          parent, attr, values)
            case 'ellipsoidgeometry':
                return EllipsoidGeometry(uuid, id_name, self.get_stamped_qualified_name(id_name, parent),
                                         parent, attr, values)
            case 'material':
                return VisualMaterial(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'transformation':
                return RigidTransformation(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case _:
                raise InvalidSemanticType
