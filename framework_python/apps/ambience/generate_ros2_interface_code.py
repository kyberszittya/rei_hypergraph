import argparse

from antlr4 import FileStream, CommonTokenStream

from rei.format.ambience.ambience_generators import extract_ambient_data_from_node_interface
from rei.format.cognilang.CogniLangLexer import CogniLangLexer
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.mapping.cognilang_file_icon import CognilangParserFileIcon
from rei.format.semantics.CognitiveEntity import AmbientNodeInterface, AmbiencePortCommunication, AmbiencePort
from rei.foundations.clock import LocalClock
from rei.hypergraph.base_elements import HypergraphEdge, HypergraphNode
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.query.query_engine import HierarchicalPrepositionQuery, HypergraphQueryEngine

from jinja2 import Template


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
    # Template
    with open("class_interface_template.templ") as f:
        code_template = ''.join(f.readlines())
    j2_template = Template(code_template)
    # Render text

    # Make directory for
    import os
    os.makedirs(root_item.id_name, exist_ok=True)
    # Iterate amibent node interface
    for r in res:
        ambience_text_data = extract_ambient_data_from_node_interface(root_item, r)

        with open(f'{root_item.id_name}/{r.id_name}.hpp', 'w') as f:
            f.write(j2_template.render(ambience_text_data))



if __name__ == "__main__":
    main()
