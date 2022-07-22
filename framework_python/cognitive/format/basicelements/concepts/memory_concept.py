import abc


class MetaMemory(metaclass=abc.ABCMeta):
    """

    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'add_element') and
                callable(cls.add_element) and
                hasattr(subclass, 'remove_element') and
                callable(cls.remove_element)
                )

    @abc.abstractmethod
    def add_element(self):
        raise NotImplementedError

    def remove_element(self):
        raise NotImplementedError


class MetaInstantaneousMemory(metaclass=MetaMemory):
    """
    Short term memory for a limited time (storing for a limited time)
    """

    @abc.abstractmethod
    def set_store_time(self, timeout: float)-> None:
        """

        :param timeout: set the maximal time an element is stored, then
        :return:
        """

class MetaStoringMemory(metaclass=MetaMemory):
    """
    Memory that stores concepts for a longer time and saves into a cache
    """

class ShortTermMemory(metaclass=MetaInstantaneousMemory):
    """

    """


class LimitedMemory(metaclass=MetaStoringMemory):
    """

    """


class BoundlessMemory(metaclass=MetaStoringMemory):
    """

    """
