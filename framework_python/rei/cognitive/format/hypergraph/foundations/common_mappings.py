from rei.cognitive.ambience.elements.communication_types import EnumCommunicationType
from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection


def map_graph_direction(arg):
    match arg.direction.text:
        case '->':
            return EnumRelationDirection.OUTWARDS
        case '<-':
            return EnumRelationDirection.INWARDS
        case '--':
            return EnumRelationDirection.UNDIRECTED


def map_communication_type(arg):
    if arg.comm_type.ambient_signal() is not None:
        return EnumCommunicationType.SIGNAL
    elif arg.comm_type.ambient_stream() is not None:
        return EnumCommunicationType.STREAM