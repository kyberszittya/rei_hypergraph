import abc

class CognitiveIcon(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def encode(self, elements):
        raise NotImplementedError