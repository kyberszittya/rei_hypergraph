import abc
import asyncio

import typing
from abc import ABC


class GraphMonad(metaclass=abc.ABCMeta):

    def __init__(self) -> None:
        super().__init__()


    @abc.abstractmethod
    async def execute(self, start) -> list[asyncio.Future]:
        raise NotImplementedError


class GraphVisitor(GraphMonad, ABC):

    def __init__(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                 filter_func: typing.Callable[[typing.Any], bool]) -> None:
        super().__init__()
        self.visitor_func = visitor_func
        self.filter_func = filter_func
