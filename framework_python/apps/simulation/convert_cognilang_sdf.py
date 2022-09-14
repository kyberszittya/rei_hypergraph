import argparse
import asyncio

from antlr4 import FileStream, CommonTokenStream

from rei.format.cognilang.CogniLangLexer import CogniLangLexer
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.mapping.cognilang_file_icon import CognilangParserFileIcon
from rei.format.mapping.cognilang_sdf_icon import CognilangSdfIcon
from rei.format.semantics.CognitiveEntity import KinematicLink, KinematicJoint, CognitiveEntity
from rei.foundations.clock import LocalClock, DummyClock
from rei.hypergraph.base_elements import HypergraphNode
from rei.query.query_engine import HierarchicalPrepositionQuery, HypergraphQueryEngine

from lxml import etree
import os


def stmt_node_depth(el, depth=2):
    if isinstance(el, HypergraphNode):
        el: HypergraphNode
        return el.depth <= depth
    return True


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
    # Instantiate visitor
    __clock = LocalClock()
    visitor = CognilangParserFileIcon("cogni_lang_file", __clock)
    visitor.visit(tree)
    root_item = visitor.root_entity
    link_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, KinematicLink),
                                              lambda x: stmt_node_depth(x, depth=2))
    joint_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, KinematicJoint),
                                               lambda x: stmt_node_depth(x, depth=1))
    cognitiveentity_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, CognitiveEntity),
                                                         lambda x: True)
    engine = HypergraphQueryEngine("engine", b'00', "engine/engine", DummyClock(), None)
    engine.add_query('link_query', link_query)
    engine.add_query('joint_query', joint_query)
    engine.add_query('cognitive_query', cognitiveentity_query)
    res = engine.execute_all_queries()
    sdf_icon = CognilangSdfIcon(DummyClock())
    asyncio.run(sdf_icon.encode(res))
    with open(os.path.join(args.output, root_item.id_name+".sdf"), 'w') as f:
        f.write(etree.tostring(sdf_icon.root_xml, pretty_print=True).decode('utf-8'))
    with open(os.path.join(args.output, root_item.id_name+".load.sh"), 'w') as f:
        f.write(f"ros2 run gazebo_ros spawn_entity.py -entity {root_item.id_name} -file {root_item.id_name}.sdf")


if __name__ == "__main__":
    main()
