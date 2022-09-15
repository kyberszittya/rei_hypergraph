from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.mapping.cognilang_mapping_errors import ErrorInvalidDirection
from rei.hypergraph.common_definitions import EnumRelationDirection


def dir_enum_relation(direction: str):
    match direction:
        case '<-':
            return EnumRelationDirection.INWARDS
        case '->':
            return EnumRelationDirection.OUTWARDS
        case '--':
            return EnumRelationDirection.BIDIRECTIONAL
    raise ErrorInvalidDirection


def extract_graphelement_signature(ctx: CogniLangParser.Graphnode_signatureContext):
    return str(ctx.ID())
