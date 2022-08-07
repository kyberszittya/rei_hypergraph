from rei.factories.foundation_factory import Sha3UniqueIdentifierGenerator
from rei.foundations.clock import DummyClock
from rei.foundations.conceptual_item import ConceptualItem


def _identification_func(x, y):
    return f"{x}.{y}"


def test_unique_identification():
    identifier = Sha3UniqueIdentifierGenerator("tester", _identification_func)
    uuid = identifier.generate_uid("test")
    assert uuid.hex() == "9c7e65446b0c0ca78980b07e8c77ae5f07051f788be634937a10b057"


def test_conceptual_item():
    identifier = Sha3UniqueIdentifierGenerator("tester", _identification_func)
    uuid = identifier.generate_uid("test")
    clock = DummyClock()
    item = ConceptualItem("test", uuid, _identification_func("tester", "test"), clock=clock)
    assert item.uuid.hex() == "9c7e65446b0c0ca78980b07e8c77ae5f07051f788be634937a10b057"
    assert item.cid == 0
    assert item.progenitor_qualified_name == "tester.test"
    assert item.cnt_subelements == 0
    assert item.parent is None


def test_conceptual_item_add_subelement():
    identifier = Sha3UniqueIdentifierGenerator("tester", _identification_func)
    clock = DummyClock()
    # Item
    uuid = identifier.generate_uid("test")
    item = ConceptualItem("test", uuid, _identification_func("tester", "test"), clock=clock)
    # Attribute testing
    assert item.uuid.hex() == "9c7e65446b0c0ca78980b07e8c77ae5f07051f788be634937a10b057"
    assert item.cid == 0
    assert item.progenitor_qualified_name == "tester.test"
    assert item.cnt_subelements == 0
    assert item.parent is None
    # Subelement
    uuid = identifier.generate_uid("test1")
    sub_item = ConceptualItem("test1", uuid, _identification_func("tester", "test1"), clock=clock)
    item.add_element(sub_item)
    assert sub_item.cid == 0
    assert item.cnt_subelements == 1
    assert sub_item.uuid.hex() != item.uuid.hex()
    assert sub_item.parent is item
    # Check qualified name
    assert sub_item.qualifed_name == "test/test1"

