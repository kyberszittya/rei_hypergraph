import asyncio

from rei.foundations.clock import DummyClock
from rei.hypergraph.base_elements import HypergraphNode
from rei.hypergraph.encoding.graph_tensor_icon import CoordinateObjectTransformer
from rei.hypergraph.encoding.graph_tensor_icon_cbor import GraphTensorCbor
from test.hypergraph.common_test_hypergraph_functions import simple_directed_graph_creation


def test_simple_tree_coo_representation():
    _, _, n0, node_list, e = simple_directed_graph_creation()
    tr = CoordinateObjectTransformer(n0)
    asyncio.run(tr.reset(n0))
    __node_list = tr.node_index_list()
    assert len(__node_list) == 4
    __edge_list = tr.edge_index_list()
    assert len(__edge_list) == 2
    asyncio.run(tr.execute())
    __val, __iout, __iin = tr.msg_value_updates()
    assert len(__val) == 4
    tr.msg_relation_index_list()


def test_simple_tree_cbor_representation():
    _, _, n0, node_list, e = simple_directed_graph_creation()
    cbor_tr = GraphTensorCbor("icon1", DummyClock(), n0)
    asyncio.run(cbor_tr.update_context(n0))
    asyncio.run(cbor_tr.update_coo())
    __msg = cbor_tr.full_msg()
    # Decode CBOR
    _new_root, _homomorphism = cbor_tr.create_graph(__msg)
    # Check new graph
    assert _new_root.id_name == n0.id_name
    assert _new_root.uuid == n0.uuid
    # Check nodes
    assert len(list(_new_root.sub_nodes)) == 3
    for i,n in enumerate(node_list):
        _n: HypergraphNode = list(_new_root.sub_nodes)[i]
        assert _n.uuid == n.uuid
        assert _n.id_name == n.id_name
    _new_edges = list(_new_root.sub_edges)
    assert '.'.join(map(lambda x: x.id_name, list(_new_edges[0].induced_subset))) == 'node0.node1'
    assert '.'.join(map(lambda x: x.id_name, list(_new_edges[1].induced_subset))) == 'node0.node2'
    # Check homomorphism
    assert _homomorphism.cnt_node == 4
    assert _homomorphism.cnt_edges == 2
    # Check bijections
    # Nodes
    assert _homomorphism.node(n0.uuid) == 0
    assert _homomorphism.node(node_list[0].uuid) == 1
    assert _homomorphism.node(node_list[1].uuid) == 2
    assert _homomorphism.node(node_list[2].uuid) == 3
    # Edges
    assert _homomorphism.edge(e[0].uuid) == 0
    assert _homomorphism.edge(e[1].uuid) == 1
