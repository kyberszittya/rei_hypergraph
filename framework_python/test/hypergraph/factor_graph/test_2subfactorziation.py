import asyncio

from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock
from rei.foundations.hierarchical_traversal_strategies import print_graph_hierarchy
from rei.hypergraph.common_definitions import EnumRelationDirection
from rei.hypergraph.factorization_operations import Factorization2Operation, MapFactorizationToFactorGraph, \
    Factorization2SubsetOperation
from rei.hypergraph.sample_graphs.fano_graph import create_fano_graph


def test_factorization2_subset_fano():
    print()
    _, __n0, __node_list, __edges = create_fano_graph("fano_test", DummyClock())
    __selected_elements = [x for x in __node_list[0:2]]
    __selected_elements.extend([x for x in __edges[0:3]])
    query = Factorization2SubsetOperation()
    rel_list = asyncio.run(query.execute(__selected_elements))
    assert len(rel_list) == 2


def test_factorization2_subset_fano_self_loop():
    print()
    _, __n0, __node_list, __edges = create_fano_graph("fano_test", DummyClock())
    __selected_elements = [x for x in __node_list[0:2]]
    __selected_elements.extend([x for x in __edges[0:3]])
    query = Factorization2SubsetOperation(True)
    rel_list = asyncio.run(query.execute(__selected_elements))
    assert len(rel_list) == 5
