from rei.format.cognilang.CogniLangParser import CogniLangParser
from rei.format.cognilang.CogniLangVisitor import CogniLangVisitor


class CognilangParserFileIcon(CogniLangVisitor):

    def visitLink(self, ctx: CogniLangParser.LinkContext):
        return super().visitLink(ctx)