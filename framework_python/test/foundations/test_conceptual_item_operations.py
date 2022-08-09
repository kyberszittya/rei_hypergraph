import pytest

from rei.foundations.common_errors import ErrorInvalidQuery
from test.foundations.common_functions_coneptual_items import _root_item_creation, _item_creation

__ITEM_FACTORY_NAME = "tester"
__ROOT_ITEM1_NAME = "test_root"
__SUB_ITEM1_NAME = "item1"
__SUB_ITEM2_NAME = "item2"
__SUB_ITEM3_NAME = "item3"
__SUB_ITEM4_NAME = "item4"
__SUB_ITEM1_1_NAME = "subitem1"


def _identification_func(x, y) -> str:
    return f"{x}/{y}"


def test_conceptual_item_retrieve():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item1.parent is item
    # Check qualified name
    assert sub_item1.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # Additional depth
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item2.parent is item
    assert sub_item2.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM2_NAME])
    _, sub_item3 = _item_creation(__SUB_ITEM3_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    # Retrieve element
    list_elem = list(item.get_element_by_id_name(__SUB_ITEM1_NAME))
    assert len(list_elem) == 1
    assert list_elem[0].uuid == sub_item1.uuid
    assert list_elem[0].id_name == __SUB_ITEM1_NAME
    # Check integrity
    assert item.cnt_subelements == 3
    # Retrieve element 2
    list_elem = list(item.get_element_by_id_name(__SUB_ITEM2_NAME))
    assert len(list_elem) == 1
    assert list_elem[0].uuid == sub_item2.uuid
    assert list_elem[0].id_name == __SUB_ITEM2_NAME
    # Retrieve element 3
    list_elem = list(item.get_element_by_id_name(__SUB_ITEM3_NAME))
    assert len(list_elem) == 1
    assert list_elem[0].uuid == sub_item3.uuid
    assert list_elem[0].id_name == __SUB_ITEM3_NAME


def test_conceptual_item_retrieve_2depth():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item1.parent is item
    # Check qualified name
    assert sub_item1.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # Additional depth
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item2.parent is item
    # Additional depth
    _, _sub_item1_1 = _item_creation(__SUB_ITEM1_1_NAME, gen_identifier, clock,
                                     __ITEM_FACTORY_NAME, _identification_func, sub_item2)
    # Retrieve subelement
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM2_NAME, __SUB_ITEM1_1_NAME])))
    assert len(l_el) == 1
    assert l_el[0].uuid == _sub_item1_1.uuid
    assert l_el[0].id_name == __SUB_ITEM1_1_NAME


def test_conceptual_item_element_unexist():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item1.parent is item
    # Check qualified name
    assert sub_item1.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # Additional depth
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item2.parent is item
    # Additional depth
    _, _sub_item1_1 = _item_creation(__SUB_ITEM1_1_NAME, gen_identifier, clock,
                                     __ITEM_FACTORY_NAME, _identification_func, sub_item2)
    # Retrieve subelement
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM2_NAME, __SUB_ITEM1_NAME])))
    assert len(l_el) == 0

#
# Deletion
#


def test_conceptual_item_delete_subelement3():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item1.parent is item
    # Check qualified name
    assert sub_item1.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # Additional depth
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item2.parent is item
    assert sub_item2.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM2_NAME])
    _, sub_item3 = _item_creation(__SUB_ITEM3_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    # Retrieve element
    list_elem = list(item.get_element_by_id_name(__SUB_ITEM1_NAME))
    assert len(list_elem) == 1
    assert list_elem[0].uuid == sub_item1.uuid
    assert list_elem[0].id_name == __SUB_ITEM1_NAME
    # Check integrity
    assert item.cnt_subelements == 3
    # Retrieve element 2
    list_elem = list(item.get_element_by_id_name(__SUB_ITEM2_NAME))
    assert len(list_elem) == 1
    assert list_elem[0].uuid == sub_item2.uuid
    assert list_elem[0].id_name == __SUB_ITEM2_NAME
    # Retrieve element 3
    list_elem = list(item.get_element_by_id_name(__SUB_ITEM3_NAME))
    assert len(list_elem) == 1
    assert list_elem[0].uuid == sub_item3.uuid
    assert list_elem[0].id_name == __SUB_ITEM3_NAME
    # Retrieve element
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM2_NAME])))
    assert len(l_el) == 1
    # Deletion
    list(item.remove_element(__SUB_ITEM2_NAME))
    assert item.cnt_subelements == 2
    # Retrieve subelement
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM2_NAME])))
    assert len(l_el) == 0


def test_conceptual_item_delete_subelement2():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item1.parent is item
    # Check qualified name
    assert sub_item1.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # Additional depth
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item2.parent is item
    assert sub_item2.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM2_NAME])
    _, sub_item3 = _item_creation(__SUB_ITEM3_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    # Deletion
    list(item.remove_element(__SUB_ITEM3_NAME))
    list(item.remove_element(__SUB_ITEM1_NAME))
    assert item.cnt_subelements == 1
    # Assert parents are null
    assert sub_item3.parent is None
    assert sub_item1.parent is None
    # Retrieve subelement
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM1_NAME])))
    assert len(l_el) == 0
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM3_NAME])))
    assert len(l_el) == 0


def test_conceptual_item_delete_subelement_then_add():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item1.parent is item
    # Check qualified name
    assert sub_item1.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # Additional depth
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item2.parent is item
    assert sub_item2.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM2_NAME])
    _, sub_item3 = _item_creation(__SUB_ITEM3_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    # Deletion
    list(item.remove_element(__SUB_ITEM3_NAME))
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM3_NAME])))
    assert len(l_el) == 0
    # Subelement 3
    _, sub_item4 = _item_creation(__SUB_ITEM4_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert item.cnt_subelements == 3
    assert sub_item4.cid == 3


def test_conceptual_item_delete_middle_subelement_then_add():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item1.parent is item
    # Check qualified name
    assert sub_item1.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # Additional depth
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item2.parent is item
    assert sub_item2.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM2_NAME])
    _, sub_item3 = _item_creation(__SUB_ITEM3_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    # Deletion
    list(item.remove_element(__SUB_ITEM2_NAME))
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM2_NAME])))
    assert len(l_el) == 0
    assert sub_item2.parent is None
    # Subelement 3
    _, sub_item4 = _item_creation(__SUB_ITEM4_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert item.cnt_subelements == 3
    assert sub_item4.cid == 3


def test_conceptual_item_delete_by_uuid():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    # Attribute testing
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item1.parent is item
    # Check qualified name
    assert sub_item1.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM1_NAME])
    # Additional depth
    _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    assert sub_item2.parent is item
    assert sub_item2.qualifed_name == '/'.join([__ROOT_ITEM1_NAME, __SUB_ITEM2_NAME])
    _, sub_item3 = _item_creation(__SUB_ITEM3_NAME, gen_identifier, clock,
                                  __ITEM_FACTORY_NAME, _identification_func, item)
    # Deletion
    list(item.remove_element(uuid=sub_item2.uuid))
    l_el = list(item.get_element_by_id_name('/'.join([__SUB_ITEM2_NAME])))
    assert len(l_el) == 0
    assert sub_item2.parent is None
    assert item.cnt_subelements == 2


def test_conceptual_item_delete_invalid_query():
    with pytest.raises(ErrorInvalidQuery):
        gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                                __ROOT_ITEM1_NAME, _identification_func)
        # Subelement
        _, sub_item1 = _item_creation(__SUB_ITEM1_NAME, gen_identifier, clock,
                                      __ITEM_FACTORY_NAME, _identification_func, item)
        # Additional depth
        _, sub_item2 = _item_creation(__SUB_ITEM2_NAME, gen_identifier, clock,
                                      __ITEM_FACTORY_NAME, _identification_func, item)
        _, sub_item3 = _item_creation(__SUB_ITEM3_NAME, gen_identifier, clock,
                                      __ITEM_FACTORY_NAME, _identification_func, item)
        # Deletion
        list(item.remove_element(id_name="", uuid=None))
        list(item.get_element_by_id_name('/'.join([__SUB_ITEM2_NAME])))
