import typing

from rei.foundations.conceptual_item import HierarchicalElement



class ValueNode(HierarchicalElement):

    def __init__(self, uuid: bytes, id_name: str, progenitor_qualified_name: str,
                 values: list[typing.Any] = None,
                 parent=None) -> None:
        super().__init__(uuid, id_name, progenitor_qualified_name, parent)
        if values is not None:
            self._values = [x for x in values]
            self.dim = len(self._values)
        else:
            self._values = []
            self.dim = 0
        # Iteration
        self._recent_element = 0

    def add_element(self, element) -> None:
        self._values.append(element)
        self.dim += 1

    def remove_element(self, id_name: str = "", uuid: bytes = None) -> typing.Generator:
        # TODO: implement it
        pass

    def get_value(self, i):
        return self._values[i]

    def update_value(self, i, arg):
        self._values[i] = arg

    def update(self):
        # TODO: implement update
        pass

    def __getitem__(self, i, /):
        return self._values[i]

    def __setitem__(self, key, value):
        self._values[key] = value

    def __iter__(self):
        return (self[i] for i in range(self.dim))

    def get_values(self):
        return [v for v in self._values]

    @property
    def val(self):
        return self._values

