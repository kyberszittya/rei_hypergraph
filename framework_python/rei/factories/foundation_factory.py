from rei.foundations.clock import MetaClock
from rei.foundations.identification.identity_generator import Sha3UniqueIdentifierGenerator
from rei.hypergraph.base_elements import HypergraphNode


class HypergraphFactory():

    def __init__(self, factory_name: str, clock: MetaClock) -> None:
        super().__init__()
        self._factory_name: str = factory_name
        self._clock: MetaClock = clock
        self.unique_identifier = Sha3UniqueIdentifierGenerator(
            self._factory_name, lambda x, y: f"{x}.{self.get_qualified_name(y.id_name)}")

    def get_qualified_name(self, name: str):
        return f"{name}.{self._clock.get_time_ns()}"

    def generate_node(self, id_name: str):
        node = HypergraphNode()

