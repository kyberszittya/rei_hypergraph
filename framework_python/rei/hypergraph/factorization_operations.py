import asyncio

from rei.foundations.graph_monad import GraphMonad


class Factorization2Operation(GraphMonad):

    async def execute(self, start) -> list[asyncio.Future]:
        pass
