from cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection


def map_graph_direction(arg):
    match arg.direction.text:
        case '->':
            return EnumRelationDirection.OUTWARDS
        case '<-':
            return EnumRelationDirection.INWARDS
        case '--':
            return EnumRelationDirection.UNDIRECTED