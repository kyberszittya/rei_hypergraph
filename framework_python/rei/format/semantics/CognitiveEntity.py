from rei.foundations.conceptual_item import HierarchicalElement
from rei.hypergraph.value_node import SemanticValueNode


class CognitiveEntity(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str,
                 parent: HierarchicalElement, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)

    def setup(self, name: str):
        self.remove_named_attribute('name')
        self.add_named_attribute('name', name)

#
# Inertia
#

class InertiaElement(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)

#
# Transformations
#

class RigidTransformation(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)


#


class KinematicGraphDefinition(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)




class KinematicLink(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)


class KinematicJoint(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)


#
# Geometry
#

class GeometryNode(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict, values):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)
        self.values = []


class CylinderGeometry(GeometryNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict, values):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr, values)


class EllipsoidGeometry(GeometryNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict, values):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr, values)


class PolyhedronGeometry(GeometryNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict, values):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr, values)

#
# Material
#

class VisualMaterial(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)


class SensorElement(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent, attr)