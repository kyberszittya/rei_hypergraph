from rei.foundations.hierarchical_traversal_strategies import DepthLimitedDepthVisitChildren
from test.foundations.common_functions_coneptual_items import _root_item_creation, _item_creation

import asyncio

from common_test_literals import __ITEM_FACTORY_NAME, __ROOT_ITEM1_NAME, \
    __CNT_BREADTH_ELEMENTS, __SUB_ITEM_PREFIX_NAME


def _identification_func(x, y) -> str:
    return f"{x}/{y}"


def test_conceptual_item_limited_depth_first_search_level2():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    item.add_elements([_item_creation(__SUB_ITEM_PREFIX_NAME+str(p), gen_identifier, clock,
                                      __ITEM_FACTORY_NAME, _identification_func, item)
                       for p in range(0, __CNT_BREADTH_ELEMENTS)])
    for it in item.get_subelements(lambda x: True):
        it.add_elements([_item_creation(__SUB_ITEM_PREFIX_NAME+str(p), gen_identifier, clock,
                                        __ITEM_FACTORY_NAME, _identification_func, it)
                         for p in range(0, __CNT_BREADTH_ELEMENTS)])
    assert item.cnt_subelements == __CNT_BREADTH_ELEMENTS
    names = []
    # Depth-limited traversal
    dlfs = DepthLimitedDepthVisitChildren(1)
    asyncio.run(dlfs.execute(item, lambda x: names.append(x.id_name), lambda x: True))
    assert '.'.join(names) == f"{__ROOT_ITEM1_NAME}.{'.'.join([__SUB_ITEM_PREFIX_NAME+str(i) for i in range(__CNT_BREADTH_ELEMENTS - 1, -1, -1)])}"
