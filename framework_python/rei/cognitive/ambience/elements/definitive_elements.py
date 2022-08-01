from enum import IntEnum

from rei.cognitive.ambience.elements.communication_types import EnumCommunicationType
from rei.cognitive.format.basicelements.concepts.network.base_definitions import NetworkRelation, EnumRelationDirection, \
    NetworkElement, NetworkNode
from rei.cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry

from rei.cognitive.format.basicelements.concepts.registry.registration_methods import InterfaceIdentifierGenerator
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode, HypergraphEdge, \
    HypergraphReferenceConnection





class AmbientGraph(HypergraphNode):
    """

    """


class SensorElement(HypergraphNode):
    """

    """


class ExteroceptiveSensor(SensorElement):
    """

    """


class ActuatorElement(HypergraphNode):
    """

    """


class AmbienceEdge(HypergraphEdge):
    """

    """

    def __init__(self, name: str, timestamp: int, parent: HypergraphNode,
                 identitygen: InterfaceIdentifierGenerator = None,
                 comm_type = EnumCommunicationType.SIGNAL):
        super().__init__(name, timestamp, parent, identitygen)
        self._communication_type = comm_type

    @property
    def communication_type(self):
        return self._communication_type

    @communication_type.setter
    def communication_type(self, arg: EnumCommunicationType):
        self._communication_type = arg


class AmbienceCommunicationConnection(HypergraphReferenceConnection):
    """

    """

    def __init__(self, name: str, timestamp: int, domain: MetaRegistry = None, parent: NetworkRelation = None,
                 endpoint: HypergraphNode = None, value=None, identitygen: InterfaceIdentifierGenerator = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED,
                 comm_type: EnumCommunicationType = EnumCommunicationType.SIGNAL):
        super().__init__(name, timestamp, domain, parent, endpoint, value, identitygen, direction)
        self._communication_type = comm_type

    @property
    def communication_type(self):
        return self._communication_type



class CommunicationPort(HypergraphNode):
    """

    """

    def __init__(self, name: str, timestamp: int, port_id: str,
                 msg_type: str, subsets: dict[bytes, NetworkElement] = None,
                 parent: NetworkNode = None, identitygen: InterfaceIdentifierGenerator = None,
                 domain: MetaRegistry = None):
        super().__init__(name, timestamp, subsets, parent, identitygen, domain)
        self._port_id: str = port_id
        self._msg_type: str = msg_type

    @property
    def port_id(self):
        return self._port_id

    @property
    def msg_type(self):
        return self._msg_type

