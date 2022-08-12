import abc
import asyncio

import typing


class GraphMonad(metaclass=abc.ABCMeta):

    def __init__(self, visitor_func: typing.Callable[[typing.Any], typing.Any],
                 filter_func: typing.Callable[[typing.Any], bool]) -> None:
        super().__init__()
        self.visitor_func = visitor_func
        self.filter_func = filter_func

    async def execute(self, start) -> list[asyncio.Future]:
        raise NotImplementedError