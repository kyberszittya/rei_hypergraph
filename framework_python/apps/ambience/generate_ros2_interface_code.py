import argparse

from antlr4 import FileStream, CommonTokenStream
from rei.format.cognilang.CogniLangLexer import CogniLangLexer
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.mapping.cognilang_file_icon import CognilangParserFileIcon
from rei.format.semantics.CognitiveEntity import AmbientNodeInterface, AmbiencePortCommunication
from rei.foundations.clock import LocalClock
from rei.hypergraph.base_elements import HypergraphEdge
from rei.query.query_engine import HierarchicalPrepositionQuery, HypergraphQueryEngine


def main():
    parser = argparse.ArgumentParser(description="Convert Cognilang to OSRF SDF")
    parser.add_argument('--input', type=str, help="Input Cognilang file")
    parser.add_argument('--output', type=str, help="Output SDF file")
    args = parser.parse_args()
    _filename = args.input
    # Parse text
    stream = FileStream(_filename)
    lexer = CogniLangLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = CogniLangParser(stream)
    tree = parser.rootnode()
    __clock = LocalClock()
    visitor = CognilangParserFileIcon("cogni_lang_file", __clock)
    visitor.visit(tree)
    # Get ambience elements
    root_item = visitor.root_entity
    ambient_port_query = HierarchicalPrepositionQuery(
        root_item, lambda x: isinstance(x, AmbientNodeInterface), lambda x: True)
    engine = HypergraphQueryEngine("engine", b'00', "engine/engine", __clock, None)
    engine.add_query('ambience_elements', ambient_port_query)
    res = engine.execute_all_queries()
    for r in res:
        r: AmbientNodeInterface
        edge: HypergraphEdge = r.parent
        items = filter(
            lambda x: x.has_item(lambda x: isinstance(x, AmbiencePortCommunication)), edge.sub_relations)



if __name__ == "__main__":
    main()
