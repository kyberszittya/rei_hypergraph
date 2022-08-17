from rei.foundations.conceptual_item import HierarchicalElement
from rei.hypergraph.value_node import SemanticValueNode


class CognitiveEntity(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str,
                 parent: HierarchicalElement, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent)
        if 'name' in attr:
            self.add_named_attribute('name', attr['name'])

    def setup(self, name: str):
        self.remove_named_attribute('name')
        self.add_named_attribute('name', name)


class KinematicGraphDefinition(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent)
        if 'name' in attr:
            self.add_named_attribute('name', attr['name'])

    def setup(self, name: str):
        self.remove_named_attribute('name')
        self.add_named_attribute('name', name)


class KinematicLink(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent)
        if 'name' in attr:
            self.add_named_attribute('name', attr['name'])

    def setup(self, name: str):
        self.remove_named_attribute('name')
        self.add_named_attribute('name', name)


class KinematicJoint(SemanticValueNode):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str, parent, attr: dict):
        super().__init__(uuid, id_name, progenitor_qualified_name, parent)
        if 'name' in attr:
            self.add_named_attribute('name', attr['name'])

    def setup(self, name: str):
        self.remove_named_attribute('name')
        self.add_named_attribute('name', name)