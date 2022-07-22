from antlr4 import *

from cognilang.CogniLangParser import CogniLangParser
from cognilang.CogniLangLexer import CogniLangLexer
from cognilang.CogniLangListener import CogniLangListener
from cognilang.CogniLangVisitor import CogniLangVisitor

import hashlib

class CognitiveEntity(object):
    name: str
    elements: dict

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}: "


class KinematicLink(object):
    name: str



class GeneratorCogniLangVisitor(CogniLangVisitor):
    root_obj: CognitiveEntity

    def visitRootnode(self, ctx: CogniLangParser.RootnodeContext):
        if len(ctx.children) == 1:
            selected_eleme = ctx.children[0]
            if isinstance(selected_eleme, CogniLangParser.EntityContext):
                self.root_obj = CognitiveEntity(
                    selected_eleme.graphnode_signature().ID())
        self.root = ctx.children
        return self.visitChildren(ctx)

    def visitLink(self, ctx: CogniLangParser.LinkContext):
        s = hashlib.sha3_224()
        s.update(str(ctx.graphnode_signature().ID()).encode('utf8'))
        print(s.hexdigest())
        return self.visitChildren(ctx)


class CustomCogniListener(CogniLangListener):

    def enterRootnode(self, ctx: CogniLangParser.RootnodeContext):
        print(ctx.children)

    def enterEntity(self, ctx:CogniLangParser.EntityContext):
        print(ctx.graphnode_signature().ID())


def main():
    stream = FileStream("D:\\Haizu\\robotics_ws\\cogni_ws\\rei_ws\\rei\\framework_python\\cognitive\\format\\hypergraph\\lang\\examples\\example_kinematic_loop.cogni")
    lexer = CogniLangLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = CogniLangParser(stream)
    tree = parser.rootnode()
    visitor = GeneratorCogniLangVisitor()
    visitor.visit(tree)


if __name__=="__main__":
    main()