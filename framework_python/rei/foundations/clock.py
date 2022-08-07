import abc
import time


class MetaClock(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_time_ns(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_time_sec(self) -> float:
        raise NotImplementedError


class DummyClock(MetaClock):

    def get_time_ns(self) -> int:
        return 0

    def get_time_sec(self) -> float:
        return 0.0


class LocalClock(MetaClock):

    def get_time_ns(self) -> int:
        return time.time_ns()

    def get_time_sec(self) -> float:
        return time.time()
