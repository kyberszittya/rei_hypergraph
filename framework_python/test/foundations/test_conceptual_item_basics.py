import pytest

from rei.foundations.common_errors import ErrorRecursiveHierarchy, ErrorDuplicateElement
from rei.foundations.conceptual_item import ConceptualItem
from rei.foundations.identification.identity_generator import Sha3UniqueIdentifierGenerator
from test.foundations.common_functions_coneptual_items import _root_item_creation, _item_creation

__ITEM_FACTORY_NAME = "tester"
__ROOT_ITEM1_NAME = "test"
__ITEM1_HEX_SHA3224_ID = "9c7e65446b0c0ca78980b07e8c77ae5f07051f788be634937a10b057"
__SUB_ITEM1_NAME = "test1"
__SUB_ITEM1_HEX_SHA3224_ID = "f0c04c26f449a82888cf62cb95fd86686e31c11c687f029defc0c1ae"
__SUB_ITEM2_NAME = "test2"
__SUB_ITEM2_HEX_SHA3224_ID = "1674986c2804d67f0d983bf4e5072b766f8eceba8911aa99aabf1e1d"


def _identification_func(x, y):
    return f"{x}.{y}"




def test_unique_identification():
    identifier = Sha3UniqueIdentifierGenerator(__ITEM_FACTORY_NAME, _identification_func)
    uuid = identifier.generate_uid(__ROOT_ITEM1_NAME)
    assert uuid.hex() == __ITEM1_HEX_SHA3224_ID


def test_conceptual_item():
    _, _, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                            __ROOT_ITEM1_NAME, _identification_func)
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ROOT_ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None


def test_conceptual_item_add_subelement():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ROOT_ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                 __ITEM_FACTORY_NAME, _identification_func)
    item.add_element(sub_item)
    assert sub_item.cid == 0
    assert item.cnt_subelements == 1
    assert sub_item.uuid.hex() != item.uuid.hex()
    assert sub_item.parent is item
    # Check qualified name
    assert sub_item.qualified_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])


def test_conceptual_item_add_subelement2():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ROOT_ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock, __ITEM_FACTORY_NAME, _identification_func)
    item.add_element(sub_item)
    assert sub_item.cid == 0
    assert item.cnt_subelements == 1
    assert sub_item.uuid.hex() != item.uuid.hex()
    assert sub_item.parent is item
    # Check qualified name
    assert sub_item.qualified_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # UUID check
    assert sub_item.uuid.hex() == __SUB_ITEM1_HEX_SHA3224_ID
    # Additional depth
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock, __ITEM_FACTORY_NAME, _identification_func)
    sub_item.add_element(sub_item1)
    assert sub_item1.parent is sub_item
    assert sub_item.cnt_subelements == 1
    assert sub_item1.qualified_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME, __SUB_ITEM1_NAME])


def test_conceptual_item_add_subelement2_2element():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ROOT_ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                 __ITEM_FACTORY_NAME, _identification_func, item)
    # Additional item
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert item.cnt_subelements == 2
    assert sub_item2.parent is item
    assert sub_item2.qualified_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM2_NAME])


def test_conceptual_item_add_subelement3_w_constructor():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.uuid.hex() == __ITEM1_HEX_SHA3224_ID
    assert item.cid == 0
    assert item.progenitor_qualified_name == ".".join([__ITEM_FACTORY_NAME, __ROOT_ITEM1_NAME])
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                 __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item.cid == 0
    assert item.cnt_subelements == 1
    assert sub_item.uuid.hex() != item.uuid.hex()
    assert sub_item.parent is item
    # Check qualified name
    assert sub_item.qualified_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # UUID check
    assert sub_item.uuid.hex() == __SUB_ITEM1_HEX_SHA3224_ID
    # Additional depth
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, sub_item)
    assert sub_item1.parent is sub_item
    assert sub_item.cnt_subelements == 1
    assert sub_item1.qualified_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME, __SUB_ITEM1_NAME])


def test_conceptual_item_add_subelement_recursion():
    with pytest.raises(ErrorRecursiveHierarchy):
        _, _, _, item = _root_item_creation(__ITEM_FACTORY_NAME, __ROOT_ITEM1_NAME, _identification_func)
        # Test recursion
        item.add_element(item)


def test_conceptual_item_add_subelement_duplicate_item():
    with pytest.raises(ErrorDuplicateElement):
        gen_identifier, _, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                             __ROOT_ITEM1_NAME, _identification_func)
        # Test recursion
        uuid = gen_identifier.generate_uid(__SUB_ITEM1_NAME)
        sub_item = ConceptualItem(__SUB_ITEM1_NAME, uuid,
                                  _identification_func(__ITEM_FACTORY_NAME, __SUB_ITEM1_NAME),
                                  clock=clock, parent=item)
        item.add_element(sub_item)
