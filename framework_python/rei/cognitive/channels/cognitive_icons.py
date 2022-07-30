import abc

from rei.cognitive.channels.channel_base_definitions import CognitiveIcon
from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkNode, NetworkElement
from rei.cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry
from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator

from cbor2 import dumps

import numpy as np

import copy


class TensorCognitiveIcon(CognitiveIcon):
    """

    """

    def __init__(self, name: str, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self._icon: np.ndarray | None = None

    def update(self, msg: np.ndarray):
        self._icon = msg

    def view(self):
        return self._icon


class ByteBufferCognitiveIcon(CognitiveIcon):
    """

    """

    def __init__(self, name: str, timestamp: int, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self._icon: bytes | None = None

    def view(self):
        return self._icon

    def update(self, msg: bytes):
        self._icon = dumps(msg)


class TextfileCognitiveIcon(CognitiveIcon):

    def __init__(self, name: str, timestamp: int, output_directory: str = "",
                 subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self.output_directory = output_directory
        self.buffer_msg = None

    @abc.abstractmethod
    def _write_to_file(self, filename: str):
        raise NotImplementedError

    def view(self):
        self._write_to_file(f"{'/'.join([self.output_directory, self.buffer_msg[0].id_name])}")

    def update(self, msg):
        self.buffer_msg = copy.copy(msg)
