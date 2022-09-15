import typing

from rei.foundations.clock import DummyClock
from rei.foundations.conceptual_item import ConceptualItem
from rei.foundations.identification.identity_generator import Sha3UniqueIdentifierGenerator

__ITEM_FACTORY_NAME = "tester"
__ROOT_ITEM1_NAME = "test_root"
__SUB_ITEM_PREFIX_NAME = "item"
__CNT_BASIC_ELEMENTS = 10
__CNT_BREADTH_ELEMENTS = 4


def _root_item_creation(factoryname: str, item_name: str,
                        identification_func: typing.Callable[[object, object], str]):
    identifier = Sha3UniqueIdentifierGenerator(factoryname, identification_func)
    uuid = identifier.generate_uid(item_name)
    clock = DummyClock()
    item = ConceptualItem(item_name, uuid, identification_func(factoryname, item_name), clock=clock)
    return identifier, uuid, clock, item


def _item_creation(name: str, gen_identifier, clock, factoryname: str,
                   identification_func: typing.Callable[[typing.Any, typing.Any], str], parent=None):
    uuid = gen_identifier.generate_uid(name)
    sub_item = ConceptualItem(name, uuid,
                              identification_func(factoryname, name),
                              clock=clock, parent=parent)
    return uuid, sub_item

