import abc


class MetaRegistrable(abc.ABCMeta):

    def __init__(self) -> None:
        super().__init__()

