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

    def generate_semantic_element(self, raw_element_type: str, id_name,
                                  parent, attr: dict[str, typing.Any], values=None):
        if len(attr) == 0:
            raise ErrorInsufficientValues
        element_type = ''.join(raw_element_type.lower().strip().split('_'))
        uuid = self.unique_identifier.generate_uid(id_name)
        el = None
        match element_type:
            case 'cognitiveentity':
                el = CognitiveEntity(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematicgraph':
                el = KinematicGraphDefinition(uuid, id_name,
                                                self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematiclink':
                el = KinematicLink(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'kinematicjoint':
                el = KinematicJoint(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'cylindergeometry':
                el = CylinderGeometry(uuid, id_name, self.get_stamped_qualified_name(id_name, parent),
                                        parent, attr, values)
            case 'polyhedrongeometry':
                el = PolyhedronGeometry(uuid, id_name, self.get_stamped_qualified_name(id_name, parent),
                                          parent, attr, values)
            case 'ellipsoidgeometry':
                el = EllipsoidGeometry(uuid, id_name, self.get_stamped_qualified_name(id_name, parent),
                                         parent, attr, values)
            case 'material':
                el = VisualMaterial(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case 'rigidtransformation':
                el = RigidTransformation(uuid, id_name, self.get_stamped_qualified_name(id_name, parent), parent, attr)
            case _:
                raise InvalidSemanticType
        if el is not None:
            parent.add_element(el)
            if values is not None:
                el.add_named_attribute("values", values)
        return el
