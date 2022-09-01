from antlr4 import FileStream, CommonTokenStream

from rei.format.cognilang.CogniLangLexer import CogniLangLexer
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.mapping.cognilang_file_icon import CognilangParserFileIcon
from rei.format.semantics.CognitiveEntity import KinematicLink, KinematicJoint, RigidTransformation, GeometryNode
from rei.foundations.clock import DummyClock
from rei.query.query_engine import HierarchicalPrepositionQuery, HypergraphQueryEngine

PENDULUM_FILENAME = "../examples/pendulum.cogni"


def test_pendulum_kinematic_links():
    stream = FileStream(PENDULUM_FILENAME)
    lexer = CogniLangLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = CogniLangParser(stream)
    tree = parser.rootnode()
    __clock = DummyClock()
    visitor = CognilangParserFileIcon("cogni_lang_file", __clock)
    visitor.visit(tree)
    root_item = visitor.root_entity
    link_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, KinematicLink))
    engine = HypergraphQueryEngine("engine", b'00', "engine/engine", DummyClock(), None)
    engine.add_query('link_query', link_query)
    res = engine.execute_all_queries()
    assert len(res) == 3


def test_pendulum_kinematic_joint_relations():
    stream = FileStream(PENDULUM_FILENAME)
    lexer = CogniLangLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = CogniLangParser(stream)
    tree = parser.rootnode()
    __clock = DummyClock()
    visitor = CognilangParserFileIcon("cogni_lang_file", __clock)
    visitor.visit(tree)
    root_item = visitor.root_entity
    link_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, KinematicJoint))
    engine = HypergraphQueryEngine("engine", b'00', "engine/engine", DummyClock(), None)
    engine.add_query('link_query', link_query)
    res = engine.execute_all_queries()
    print(res)
    assert len(res) == 6


def test_pendulum_kinematic_rigid_transformation():
    stream = FileStream(PENDULUM_FILENAME)
    lexer = CogniLangLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = CogniLangParser(stream)
    tree = parser.rootnode()
    __clock = DummyClock()
    visitor = CognilangParserFileIcon("cogni_lang_file", __clock)
    visitor.visit(tree)
    root_item = visitor.root_entity
    link_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, RigidTransformation))
    engine = HypergraphQueryEngine("engine", b'00', "engine/engine", DummyClock(), None)
    engine.add_query('link_query', link_query)
    res = engine.execute_all_queries()
    print(res)
    assert len(res) == 4


def test_pendulum_kinematic_geometry_nodes():
    stream = FileStream(PENDULUM_FILENAME)
    lexer = CogniLangLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = CogniLangParser(stream)
    tree = parser.rootnode()
    __clock = DummyClock()
    visitor = CognilangParserFileIcon("cogni_lang_file", __clock)
    visitor.visit(tree)
    root_item = visitor.root_entity
    link_query = HierarchicalPrepositionQuery(root_item, lambda x: isinstance(x, GeometryNode))
    engine = HypergraphQueryEngine("engine", b'00', "engine/engine", DummyClock(), None)
    engine.add_query('link_query', link_query)
    res = engine.execute_all_queries()
    print(res)
    assert len(res) == 3
