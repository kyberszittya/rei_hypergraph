from cognitive.format.basicelements.concepts.registry.base_definitions import MetaRegistry, \
    EnumRegistryOperationResult, MetaRegistrable, ErrorRegistry


class NetworkTaxonomy(MetaRegistry):
    """
    Taxonomy of network item
    """

    def __init__(self, name: str, timestamp: int):
        super().__init__(name, timestamp)
        self._cnt_registered_item: int = 0
        self.registered_items: dict[bytes, MetaRegistrable] = {}

    def item_register(self, item: MetaRegistrable, timestamp: int) -> EnumRegistryOperationResult:
        # Check whether the registry is itself
        if item is self:
            return EnumRegistryOperationResult.REGISTRY_LOOP
        qualified_name = '/'.join([self.qualified_name, item.name])
        # Check for duplicates
        if qualified_name in set([s.name for s in self.registered_items.values()]) \
                or item.uuid in self.registered_items.keys():
            return EnumRegistryOperationResult.DUPLICATE
        n_uuid = self.generate_domain_uid()
        item._uuid = n_uuid
        item.set_parent(self)
        item.update_qualified_name()
        self.registered_items[self.generate_domain_uid()] = item
        self._cnt_registered_item += 1
        return EnumRegistryOperationResult.CONFIRMED

    def generate_domain_uid(self) -> bytes:
        return self._cnt_registered_item.to_bytes(
            self._cnt_registered_item // 8 + 7, byteorder='big')

    def register(self, registry: MetaRegistry, timestamp: int):
        """
        Register the taxonomy to another taxonomy

        :param registry:
        :param timestamp:
        :return:
        """
        match registry.item_register(self, timestamp):
            case EnumRegistryOperationResult.CONFIRMED:
                self.set_parent(registry)
            case EnumRegistryOperationResult.REGISTRY_LOOP:
                raise ErrorRegistry("Element is registered to itself")
            case EnumRegistryOperationResult.DUPLICATE:
                raise ErrorRegistry("Duplicate element detected")

    def item_deregister(self, item: MetaRegistrable) -> EnumRegistryOperationResult:
        if len(self.registered_items) != 0:
            self.registered_items.pop(item.uuid)
            self._cnt_registered_item -= 1
            item.update_qualified_name()
            return EnumRegistryOperationResult.CONFIRMED
        else:
            return EnumRegistryOperationResult.EMPTY_REGISTRY

    def deregister(self):
        self._parent_registry.item_deregister(self)
        self._parent_registry = None
        self._qualified_name = self.name
        self._uuid = None

    def reregister(self, new_registy: MetaRegistry, timestamp: int):
        self.deregister()
        self.register(new_registy, timestamp)

    def update_qualified_name(self):
        super(NetworkTaxonomy, self).update_qualified_name()
        for v in self.registered_items.values():
            if isinstance(v, MetaRegistrable):
                v.update_qualified_name()


class NetworkRegistryItem(MetaRegistrable):
    """
    An item which is registered as a part of a simple network-like item
    """

    def __init__(self, name: str, timestamp: int):
        super().__init__(name, timestamp)

    def deregister(self):
        self._parent_registry.item_deregister(self)
        self._parent_registry = None
        self._qualified_name = self.name
        self._uuid = None

    def reregister(self, new_registry: MetaRegistry, timestamp: int):
        self.deregister()
        self.register(new_registry, timestamp)

    def register(self, registry: MetaRegistry, timestamp: int):

        self._registration_timestamp = timestamp
        match registry.item_register(self, timestamp):
            case EnumRegistryOperationResult.CONFIRMED:
                pass
            case EnumRegistryOperationResult.DUPLICATE:
                raise ErrorRegistry("Duplicate element detected")
