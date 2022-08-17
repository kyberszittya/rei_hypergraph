from rei.foundations.clock import MetaClock
from rei.foundations.conceptual_item import HierarchicalElement
from rei.foundations.identification.identity_generator import Sha3UniqueIdentifierGenerator


class ErrorInsufficientValues(Exception):
    pass

class AbstractElementFactory():

    def __init__(self, factory_name: str, clock: MetaClock) -> None:
        super().__init__()
        self._factory_name: str = factory_name
        self._clock: MetaClock = clock
        self.unique_identifier = Sha3UniqueIdentifierGenerator(
            self._factory_name, lambda x, y: f"{x}/{self.get_qualified_name(y)}")

    def get_qualified_name(self, name: str):
        return f"{name}.{self._clock.get_time_ns()}"

    def get_stamped_qualified_name(self, id_name: str, parent: HierarchicalElement):
        return '/'.join([parent.qualified_name, id_name]) + f".{self._clock.get_time_ns()}",
