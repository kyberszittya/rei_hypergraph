from rei.foundations.hierarchical_traversal_strategies import BreadthFirstHierarchicalTraversal, \
    DepthFirstHierarchicalTraversal
from test.foundations.common_functions_conceptual_items import _root_item_creation, _item_creation, \
    __ITEM_FACTORY_NAME, __ROOT_ITEM1_NAME, __CNT_BASIC_ELEMENTS, __CNT_BREADTH_ELEMENTS, __SUB_ITEM_PREFIX_NAME
import asyncio


def _identification_func(x, y) -> str:
    return f"{x}/{y}"


def test_conceptual_item_multiple_add():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    s_ids = [__SUB_ITEM_PREFIX_NAME + str(i) for i in range(__CNT_BASIC_ELEMENTS)]
    items = [_item_creation(p, gen_identifier, clock, __ITEM_FACTORY_NAME, _identification_func, item)
             for p in s_ids]
    asyncio.get_event_loop().run_until_complete(item.add_elements(items))
    assert item.cnt_subelements == __CNT_BASIC_ELEMENTS
    for it in s_ids:
        res = list(item.get_element_by_id_name(it))
        assert len(res) == 1
        assert res[0].parent is item


def test_conceptual_item_multiple_remove():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    item.add_elements([_item_creation(__SUB_ITEM_PREFIX_NAME+str(p), gen_identifier, clock,
                                      __ITEM_FACTORY_NAME, _identification_func, item)
                       for p in range(0, __CNT_BASIC_ELEMENTS)])
    assert item.cnt_subelements == __CNT_BASIC_ELEMENTS
    s_ids_removable = [__SUB_ITEM_PREFIX_NAME + str(i) for i in range(0, __CNT_BASIC_ELEMENTS, 2)]
    rem = zip(s_ids_removable, [None for _ in range(0, __CNT_BASIC_ELEMENTS, 2)])
    # Parallel execution
    asyncio.get_event_loop().run_until_complete(item.remove_elements(tuple(rem)))
    assert item.cnt_subelements == 5
    # Check remaining element
    for it in s_ids_removable:
        res = list(item.get_element_by_id_name(it))
        assert len(res) == 0


def test_conceptual_item_breadth_first_search():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    item.add_elements([_item_creation(__SUB_ITEM_PREFIX_NAME+str(p), gen_identifier, clock,
                                      __ITEM_FACTORY_NAME, _identification_func, item)
                       for p in range(0, __CNT_BREADTH_ELEMENTS)])
    assert item.cnt_subelements == __CNT_BREADTH_ELEMENTS
    names = []
    # Run hierarchical traversal
    bfs = BreadthFirstHierarchicalTraversal(lambda x: names.append(x.id_name), lambda x: True)
    asyncio.run(bfs.execute(item))
    assert '.'.join(names) == f"{__ROOT_ITEM1_NAME}.{'.'.join([__SUB_ITEM_PREFIX_NAME+str(i) for i in range(0, __CNT_BREADTH_ELEMENTS)])}"


def test_conceptual_item_breadth_first_search_level2():
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
    # Run hierarchical traversal
    bfs = BreadthFirstHierarchicalTraversal(lambda x: names.append(x.id_name), lambda x: True)
    asyncio.run(bfs.execute(item))
    assert '.'.join(names) == __ROOT_ITEM1_NAME+''.join(5*('.'+'.'.join([__SUB_ITEM_PREFIX_NAME+str(i) for i in range(0, __CNT_BREADTH_ELEMENTS)])))


def test_conceptual_item_depth_first_search():
    gen_identifier, uuid, clock, item = _root_item_creation(__ITEM_FACTORY_NAME,
                                                            __ROOT_ITEM1_NAME, _identification_func)
    item.add_elements([_item_creation(__SUB_ITEM_PREFIX_NAME+str(p), gen_identifier, clock,
                                      __ITEM_FACTORY_NAME, _identification_func, item)
                       for p in range(0, __CNT_BREADTH_ELEMENTS)])
    assert item.cnt_subelements == __CNT_BREADTH_ELEMENTS
    names = []
    # Ru  hierarchical traversal
    dfs = DepthFirstHierarchicalTraversal(lambda x: names.append(x.id_name), lambda x: True)
    asyncio.run(dfs.execute(item))
    assert '.'.join(names) == f"{__ROOT_ITEM1_NAME}.{'.'.join([__SUB_ITEM_PREFIX_NAME+str(i) for i in range(__CNT_BREADTH_ELEMENTS - 1, -1, -1)])}"
