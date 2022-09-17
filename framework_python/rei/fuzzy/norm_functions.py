import asyncio

import numpy as np

from rei.foundations.graph_monad import GraphMonad
from rei.hypergraph.base_elements import HypergraphNode


class SNorm(GraphMonad):

    async def execute(self, start) -> list[asyncio.Future]:
        raise NotImplementedError


class MaxNorm(SNorm):

    async def execute(self, start) -> list[asyncio.Future]:
        return np.max(start)


class TNorm(GraphMonad):

    async def execute(self, start) -> list[asyncio.Future]:
        raise NotImplementedError


class MinNorm(SNorm):

    async def execute(self, start) -> list[asyncio.Future]:
        return np.min(start)
