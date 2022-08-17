import argparse

from antlr4 import FileStream, CommonTokenStream

from rei.factories.foundation_factory import HypergraphFactory
from rei.format.cognilang.CogniLangLexer import CogniLangLexer
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.mapping.cognilang_file_icon import CognilangParserFileIcon
from rei.foundations.clock import LocalClock


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
    print(visitor.root_entity.id_name)


if __name__ == "__main__":
    main()
