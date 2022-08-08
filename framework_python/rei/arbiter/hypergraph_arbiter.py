from rei.foundations.clock import MetaClock
from rei.foundations.conceptual_item import ConceptualItem, HierarchicalElement


class HypergraphElement(ConceptualItem):
    """
    
    """

    def __init__(self, id_name: str, uuid: bytes, qualified_name: str, clock: MetaClock,
                 parent: HierarchicalElement = None) -> None:
        super().__init__(id_name, uuid, qualified_name, clock, parent)


class HypergraphNode(HypergraphElement):
    """

    """


