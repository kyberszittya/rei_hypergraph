import abc
import asyncio

import typing


class GraphMonad(metaclass=abc.ABCMeta):

    def execute(self, start, visitor_func: typing.Callable[[typing.Any], typing.Any],
                filter_func: typing.Callable[[typing.Any], bool]) -> list[asyncio.Future]:
        raise NotImplementedError