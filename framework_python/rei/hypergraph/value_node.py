import typing

from rei.foundations.conceptual_item import HierarchicalElement


class ValueNode(HierarchicalElement):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str,
                 values: list[typing.Any] = None,
                 parent=None) -> None:
        super().__init__(uuid, id_name, progenitor_qualified_name, parent)
        if values is not None:
            self._values = [x for x in values]
        else:
            self._values = []

    def add_element(self, element) -> None:
        self._values.append(element)

    def remove_element(self, id_name: str = "", uuid: bytes = None) -> typing.Generator:
        pass

    def get_value(self, i):
        return self._values[i]

    def update_value(self, i, arg):
        self._values[i] = arg

    def update(self):
        pass

    def __getitem__(self, i, /):
        return self._values[i]
