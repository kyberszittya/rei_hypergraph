import argparse

from antlr4 import FileStream, CommonTokenStream
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
    ambience_text_data = {}
    for r in res:
        r: AmbientNodeInterface
        edge: HypergraphEdge = r.parent
        class_name = ''.join([x.capitalize() for x in r.id_name.split('_')])
        ambience_text_data["class_name"] = class_name
        ambience_text_data["pub_ambience_ports"] = []
        ambience_text_data["sub_ambience_ports"] = []
        file_name = '_'.join([root_item.id_name.upper(), r.id_name.upper()])
        ambience_text_data["file_name"] = file_name
        items = filter(lambda x: x.has_item(lambda x: isinstance(x, AmbiencePortCommunication)), edge.sub_relations)
        for i in items:
            n: HypergraphNode = i.endpoint
            port: AmbiencePort = next(n.get_element_by_id_name(n.id_name))
            msg_type = port.get_id_name_from_attribute("msgtype").replace('"', '').strip()
            msg_type = msg_type.split("/")
            # Class name
            port_name = ''.join([x.capitalize() for x in port.get_id_name_from_attribute("name").split('_')])
            match i.direction:
                case EnumRelationDirection.OUTWARDS:
                    ambience_text_data["pub_ambience_ports"].append((port_name, "::".join(msg_type),
                                                                     port.get_id_name_from_attribute("topicname")))
                case EnumRelationDirection.INWARDS:
                    ambience_text_data["sub_ambience_ports"].append((port_name, "::".join(msg_type),
                                                                     port.get_id_name_from_attribute("topicname")))
        with open(f'{r.id_name}.hpp', 'w') as f:
            f.write(j2_template.render(ambience_text_data))



if __name__ == "__main__":
    main()
