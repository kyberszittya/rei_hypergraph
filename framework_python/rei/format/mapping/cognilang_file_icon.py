from rei.factories.foundation_factory import HypergraphFactory
from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.cognilang.CogniLangVisitor import CogniLangVisitor


class ErrorParserNoFactorySet(Exception):
    pass


class CognilangParserFileIcon(CogniLangVisitor):

    def __init__(self, element_factory: HypergraphFactory):
        super().__init__()
        self._element_cache = {}
        self.__factory = element_factory

    def visitLink(self, ctx: CogniLangParser.LinkContext):
        return super().visitLink(ctx)

    def visitRootnode(self, ctx: CogniLangParser.RootnodeContext):
        if self.__factory is None:
            raise ErrorParserNoFactorySet
        return self.visitChildren(ctx)

    def visitEntity(self, ctx: CogniLangParser.EntityContext):
        name = str(ctx.graphnode_signature().ID())
        print(name)
        return self.visitChildren(ctx)



