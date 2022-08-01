from rei.cognitive.channels.channel_base_definitions import CognitiveChannelDendrite
from rei.cognitive.channels.cognitive_icons import TextfileCognitiveIcon
from rei.cognitive.entities.entity.cognitiveentity import CognitiveEntity
from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkElement, NetworkNode, \
    NetworkRelation, EnumRelationDirection
from rei.cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode


class AmbienceDendrite(CognitiveChannelDendrite):

    def __init__(self, name: str, timestamp: int, domain: MetaRegistry = None, parent: NetworkRelation = None,
                 endpoint: HypergraphNode = None, value=None, identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, domain, parent, endpoint, value, identitygen, direction)

    def encode(self, arg: CognitiveEntity) -> []:
        return arg.subset_elements

    def decode(self, arg):
        pass


class CodeGenerationIcon(TextfileCognitiveIcon):

    def __init__(self, name: str, timestamp: int, output_directory: str = "",
                 subsets: dict[bytes, NetworkElement] = None, parent: NetworkNode = None,
                 identitygen: InterfaceIdentifierGenerator = None, domain: MetaRegistry = None):
        super().__init__(name, timestamp, output_directory, subsets, parent, identitygen, domain)

    def _write_to_file(self, filename: str):
        pass

