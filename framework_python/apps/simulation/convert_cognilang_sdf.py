import argparse
import asyncio

from antlr4 import FileStream, CommonTokenStream

from rei.format.cognilang.CogniLangLexer import CogniLangLexer
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.mapping.cognilang_file_icon import CognilangParserFileIcon
from rei.format.mapping.cognilang_sdf_icon import CognilangSdfIcon
from rei.format.semantics.CognitiveEntity import KinematicLink, KinematicJoint, CognitiveEntity
from rei.foundations.clock import LocalClock, DummyClock
from rei.query.query_engine import HierarchicalPrepositionQuery, HypergraphQueryEngine

from lxml import etree


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
    link_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, KinematicLink))
    joint_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, KinematicJoint))
    cognitiveentity_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, CognitiveEntity))
    engine = HypergraphQueryEngine("engine", b'00', "engine/engine", DummyClock(), None)
    engine.add_query('link_query', link_query)
    engine.add_query('joint_query', joint_query)
    engine.add_query('cognitive_query', cognitiveentity_query)
    res = engine.execute_all_queries()
    sdf_icon = CognilangSdfIcon()
    asyncio.run(sdf_icon.encode(res))
    print(etree.tostring(sdf_icon.root_xml, pretty_print=True).decode('utf-8'))
    #asyncio.run(bfs.execute(root_item))


if __name__ == "__main__":
    main()
