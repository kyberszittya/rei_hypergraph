import abc
from enum import IntEnum

from cognitive.format.basicelements.concepts.registry.base_definitions import \
    MetaRegistry, MetaRegistrable, \
    EnumRegistryOperationResult
from cognitive.format.basicelements.concepts.registry.registration_methods import \
    InterfaceIdentifierGenerator, IdentifierGeneratorSha224
from cognitive.format.basicelements.concepts.network.taxonomy import \
    NetworkTaxonomy, NetworkRegistryItem
from cognitive.format.basicelements.concepts.identification.base_definitions import \
    MetaIdentifiable


class EnumRelationDirection(IntEnum):
    UNDIRECTED = 0
    OUTWARDS = -1
    INWARDS = 1


class NetworkElement(MetaIdentifiable):
    """
    A network element (e.g., edge node).
    All network element can be uniquely defined.

    All network element can contain the following:
    - Registrable concepts
    - Classification concepts
    - Definitive concepts

    """

    def __init__(self, name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator,
                 domain: MetaRegistry, parent = None):
        super().__init__(name, timestamp, identitygen)
        # Registrable concepts
        self.registrables: list[MetaRegistrable] = []
        # Set parent
        self._parent = parent
        # Set prefix
        prefix = ""
        if domain is not None:
            self.domain = domain
            prefix = domain.name
        self.parent: NetworkElement = parent

        if identitygen is None:
            super().__init__(name, timestamp, IdentifierGeneratorSha224(prefix=prefix))
        else:
            super().__init__(name, timestamp, identitygen)
        self.register(self.domain, timestamp)
        # Subset
        self._subsets: dict[bytes, NetworkElement] = {}



    @abc.abstractmethod
    def register(self, domain: MetaRegistry, timestamp: int) -> EnumRegistryOperationResult:
        """
        Register network element in a registry

        :param domain: the registry where the item is registered
        :param timestamp: the time of registration
        :return: registry operation result
        """
        raise NotImplementedError

    @property
    def progenitor_registry(self):
        """
        Main item that had been registered for this item

        :return:
        """
        if len(self.registrables) == 0:
            return None
        return self.registrables[0]





class EnumNodeType(IntEnum):
    ORDINARY = 0
    SUPER_TAXON_ROOT = 1


class NetworkNode(NetworkElement):
    """
    A network node that can be organized as a part of a network.
    All semantic network nodes can be uniquely identified.



    Furthermore, a network node can contain the following:
    - Registrable concepts
    - Classification concepts
    - Definitive concepts
    - Naming concepts
    """

    def __init__(self, name: str, timestamp: int,
                 identitygen: InterfaceIdentifierGenerator,
                 domain: MetaRegistry, parent: NetworkElement = None):
        self._taxonomy = NetworkTaxonomy(name, timestamp)
        self._node_type: EnumNodeType = EnumNodeType.ORDINARY
        if domain is None:
            self.domain = self._taxonomy
            self._node_type = EnumNodeType.SUPER_TAXON_ROOT
        super().__init__(name, timestamp, identitygen, domain, parent)
        self._parent_node = False



    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, arg):
        self._parent = arg

    def register(self, domain: MetaRegistry, timestamp: int):
       # A statemachine between ORDINARY and SUPER_TAXON_ROOT node types
       match self._node_type:
            case EnumNodeType.ORDINARY:
                if len(self.registrables) == 0:
                    self.registrables.append(self._taxonomy)
                    self.registrables[0].register(domain, timestamp)
                else:
                    # Transitions
                    if domain is not self._taxonomy:
                        # ORDINARY-ORDINARY
                        self.registrables[0].deregister()
                        self.registrables[0].register(domain, timestamp)
                    else:
                        # ORDINARY->SUPER_TAXON_ROOT
                        self.registrables[0].deregister()
                        self._node_type = EnumNodeType.SUPER_TAXON_ROOT
            case EnumNodeType.SUPER_TAXON_ROOT:
                if len(self.registrables) == 0:
                    self.registrables.append(self._taxonomy)
                else:
                    # Transitions
                    if domain is not self._taxonomy:
                        self._node_type = EnumNodeType.ORDINARY
                        self.registrables[0].register(domain, timestamp)
                    else:
                        self.registrables[0].deregister()
                        self.registrables[0] = self._taxonomy
       # Update domain
       self.domain = domain



class NetworkRelation(NetworkElement):
    """
    A relation between nodes.

    NOTE: not necessarily binary relation (metaclass of hyperedges as well)

    """

    def __init__(self, name: str, timestamp: int,
                 domain: MetaRegistry, identitygen: InterfaceIdentifierGenerator,
                 parent: NetworkElement = None,
                 direction: EnumRelationDirection = EnumRelationDirection.UNDIRECTED):
        super().__init__(name, timestamp, identitygen, domain, parent)

        self._direction = direction


    @property
    def direction(self):
        return self._direction

    def register(self, domain: MetaRegistry, timestamp: int):
        # Node name is the first registrable item
        if len(self.registrables) == 0:
            self.registrables.append(NetworkRegistryItem(self._id_name, self._timestamp))
            self.registrables[0].register(domain, timestamp)
        else:
            self.registrables[0].deregister()
            self.registrables[0].register(domain, timestamp)
        self.domain = domain
