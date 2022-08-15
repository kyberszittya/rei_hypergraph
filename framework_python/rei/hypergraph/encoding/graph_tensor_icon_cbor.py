
from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import MetaClock
from rei.hypergraph.base_elements import HypergraphNode, HypergraphEdge, HypergraphRelation
from rei.hypergraph.encoding.graph_tensor_icon import CoordinateObjectTransformer

import cbor2

from rei.hypergraph.homomorphism_functions import IndexHomomorphismGraphTensor
from rei.hypergraph.value_node import ValueNode


class GraphTensorCbor(object):

    def __init__(self, icon_name: str, clock: MetaClock, context: HypergraphNode):
        self._coo_tr: CoordinateObjectTransformer = CoordinateObjectTransformer(context)
        self.__clock = clock
        self.__icon_name = icon_name
        # Store last decoded graph & homomorphism
        self._context: HypergraphNode | None = None
        self._homomorphism: IndexHomomorphismGraphTensor | None = None

    async def update_context(self, context: HypergraphNode):
        return await self._coo_tr.reset(context)

    async def update_coo(self):
        return await self._coo_tr.execute()

    def full_msg(self):
        msg = self._coo_tr.msg_tensor_value_updates()
        # Message fragment
        frag = [self._coo_tr.node_index_list(),
                self._coo_tr.edge_index_list(),
                self._coo_tr.msg_relation_index_list(),
                self._coo_tr.msg_value_nodes(),
                msg[0], msg[1], msg[2]]
        return cbor2.dumps(frag)

    def msg_value_update(self):
        return cbor2.dumps(self._coo_tr.msg_value_node_update())

    def from_msg_update_values(self, msg: bytes):
        frag = cbor2.loads(msg)
        for v in frag:
            self._context[self._homomorphism.ival(v[0])].update_values(v[1])

    def create_graph(self, msg: bytes):
        frag = cbor2.loads(msg)
        # Get messages
        __factory = HypergraphFactory(self.__icon_name, self.__clock)
        # Cache parents
        _elements = {}
        _root = None
        # Nodes
        nodes = []
        for n in frag[0]:
            _el = HypergraphNode(n[1], n[0], n[4].decode('utf-8'), self.__clock)
            # Add to cache
            _elements[n[0]] = _el
            if n[3] == 0:
                _root = _el
            else:
                _elements[n[3]].add_element(_el)
            nodes.append((n[0], n[2]))
        # Edges
        edges = []
        for e in frag[1]:
            _el = HypergraphEdge(e[1], e[0], e[4].decode('utf-8'), self.__clock, _elements[e[3]])
            _elements[e[0]] = _el
            edges.append((e[0], e[2]))
        # Relation
        for rel in frag[2]:
            _el = HypergraphRelation(rel[0], rel[1], rel[2], _elements[rel[4]], None, parent=_elements[rel[5]])
            _elements[rel[5]].add_element(_el)
        # Value nodes
        values = []
        for v in frag[3]:
            _el = ValueNode(v[0], v[1], v[4], v[5])
            values.append((v[0], v[2]))
            _elements[v[3]].add_element(_el)
        # Value tensor
        # Setup homomorphism
        _homomorphism = IndexHomomorphismGraphTensor(True)
        _homomorphism.reset_from_bijection(nodes, edges, values)
        # Delete hypergraph element cache
        del _elements
        del __factory
        # Delete cache lists
        del nodes
        del edges
        del values
        # Store results locally
        self._context = _root
        self._homomorphism = _homomorphism
        # Return
        return _root, _homomorphism
