import argparse

from antlr4 import FileStream, CommonTokenStream

from rei.format.cognilang.CogniLangLexer import CogniLangLexer
from rei.format.cognilang.CogniLangParser import CogniLangParser


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

if __name__ == "__main__":
    main()
