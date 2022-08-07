import pytest

from rei.factories.foundation_factory import Sha3UniqueIdentifierGenerator
from rei.foundations.clock import DummyClock
from rei.foundations.common_errors import ErrorRecursiveHierarchy, ErrorDuplicateElement
from rei.foundations.conceptual_item import ConceptualItem


__ITEM_FACTORY_NAME = "tester"
__ITEM1_NAME = "test"
__ITEM1_HEX_SHA3224_ID = "9c7e65446b0c0ca78980b07e8c77ae5f07051f788be634937a10b057"
__SUB_ITEM1_NAME = "test1"
__SUB_ITEM1_HEX_SHA3224_ID = "f0c04c26f449a82888cf62cb95fd86686e31c11c687f029defc0c1ae"
__SUB_ITEM2_NAME = "test2"
__SUB_ITEM2_HEX_SHA3224_ID = "1674986c2804d67f0d983bf4e5072b766f8eceba8911aa99aabf1e1d"


def _identification_func(x, y):
    return f"{x}.{y}"


def _root_item_creation():
    identifier = Sha3UniqueIdentifierGenerator(__ITEM_FACTORY_NAME, _identification_func)
    uuid = identifier.generate_uid(__ITEM1_NAME)
    clock = DummyClock()
    item = ConceptualItem(__ITEM1_NAME, uuid,
                          _identification_func(__ITEM_FACTORY_NAME, __ITEM1_NAME), clock=clock)
    return identifier, uuid, clock, item


def _item_creation(name: str, gen_identifier, clock, parent=None):
    uuid = gen_identifier.generate_uid(name)
    sub_item = ConceptualItem(name, uuid,
                              _identification_func(__ITEM_FACTORY_NAME, name),
                              clock=clock, parent=parent)
    return uuid, sub_item


def test_unique_identification():
    identifier = Sha3UniqueIdentifierGenerator(__ITEM_FACTORY_NAME, _identification_func)
    uuid = identifier.generate_uid(__ITEM1_NAME)
    assert uuid.hex() == __ITEM1_HEX_SHA3224_ID


def test_conceptual_item():
    _, _, clock, item = _root_item_creation()
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None


def test_conceptual_item_add_subelement():
    gen_identifier, uuid, clock, item = _root_item_creation()
    # Attribute testing
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock)
    item.add_element(sub_item)
    assert sub_item.cid == 0
    assert item.cnt_subelements == 1
    assert sub_item.uuid.hex() != item.uuid.hex()
    assert sub_item.parent is item
    # Check qualified name
    assert sub_item.qualifed_name == '/'.join([__ITEM1_NAME, __SUB_ITEM1_NAME])


def test_conceptual_item_add_subelement2():
    gen_identifier, uuid, clock, item = _root_item_creation()
    # Attribute testing
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    uuid = gen_identifier.generate_uid(__SUB_ITEM1_NAME)
    sub_item = ConceptualItem(__SUB_ITEM1_NAME, uuid,
                              _identification_func(__ITEM_FACTORY_NAME, __SUB_ITEM1_NAME), clock=clock)
    item.add_element(sub_item)
    assert sub_item.cid == 0
    assert item.cnt_subelements == 1
    assert sub_item.uuid.hex() != item.uuid.hex()
    assert sub_item.parent is item
    # Check qualified name
    assert sub_item.qualifed_name == '/'.join([__ITEM1_NAME, __SUB_ITEM1_NAME])
    # UUID check
    assert sub_item.uuid.hex() == __SUB_ITEM1_HEX_SHA3224_ID
    # Additional depth
    uuid = gen_identifier.generate_uid(__SUB_ITEM1_NAME)
    sub_item1 = ConceptualItem(__SUB_ITEM1_NAME, uuid,
                              _identification_func(__ITEM_FACTORY_NAME, __SUB_ITEM1_NAME), clock=clock)
    sub_item.add_element(sub_item1)
    assert sub_item1.parent is sub_item
    assert sub_item.cnt_subelements == 1
    assert sub_item1.qualifed_name == '/'.join([__ITEM1_NAME, __SUB_ITEM1_NAME, __SUB_ITEM1_NAME])


def test_conceptual_item_add_subelement2_2element():
    gen_identifier, uuid, clock, item = _root_item_creation()
    # Attribute testing
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    uuid = gen_identifier.generate_uid(__SUB_ITEM1_NAME)
    sub_item = ConceptualItem(__SUB_ITEM1_NAME, uuid,
                              _identification_func(__ITEM_FACTORY_NAME, __SUB_ITEM1_NAME), clock=clock)
    item.add_element(sub_item)
    # Additional item
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock, item)
    assert item.cnt_subelements == 2
    assert sub_item2.parent is item
    assert sub_item2.qualifed_name == '/'.join([__ITEM1_NAME, __SUB_ITEM2_NAME])


def test_conceptual_item_add_subelement3_w_constructor():
    gen_identifier, uuid, clock, item = _root_item_creation()
    # Attribute testing
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    uuid = gen_identifier.generate_uid(__SUB_ITEM1_NAME)
    sub_item = ConceptualItem(__SUB_ITEM1_NAME, uuid,
                              _identification_func(__ITEM_FACTORY_NAME, __SUB_ITEM1_NAME),
                              clock=clock, parent=item)
    assert sub_item.cid == 0
    assert item.cnt_subelements == 1
    assert sub_item.uuid.hex() != item.uuid.hex()
    assert sub_item.parent is item
    # Check qualified name
    assert sub_item.qualifed_name == '/'.join([__ITEM1_NAME, __SUB_ITEM1_NAME])
    # UUID check
    assert sub_item.uuid.hex() == __SUB_ITEM1_HEX_SHA3224_ID
    # Additional depth
    uuid = gen_identifier.generate_uid(__SUB_ITEM1_NAME)
    sub_item1 = ConceptualItem(__SUB_ITEM1_NAME, uuid,
                               _identification_func(__ITEM_FACTORY_NAME, __SUB_ITEM1_NAME),
                               clock=clock, parent=sub_item)
    assert sub_item1.parent is sub_item
    assert sub_item.cnt_subelements == 1
    assert sub_item1.qualifed_name == '/'.join([__ITEM1_NAME, __SUB_ITEM1_NAME, __SUB_ITEM1_NAME])


def test_conceptual_item_add_subelement_recursion():
    with pytest.raises(ErrorRecursiveHierarchy):
        _, _, _, item = _root_item_creation()
        # Test recursion
        item.add_element(item)


def test_conceptual_item_add_subelement_duplicate_item():
    with pytest.raises(ErrorDuplicateElement):
        gen_identifier, _, clock, item = _root_item_creation()
        # Test recursion
        uuid = gen_identifier.generate_uid(__SUB_ITEM1_NAME)
        sub_item = ConceptualItem(__SUB_ITEM1_NAME, uuid,
                                  _identification_func(__ITEM_FACTORY_NAME, __SUB_ITEM1_NAME),
                                  clock=clock, parent=item)
        item.add_element(sub_item)
