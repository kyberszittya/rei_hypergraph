from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import DummyClock
from rei.hypergraph.base_elements import HypergraphNode
from rei.hypergraph.common_definitions import EnumRelationDirection


#
# Segment: FANO GRAPH
#


def create_fano_graph():
    __clock = DummyClock()
    __factory = HypergraphFactory("test", __clock)
    test_system = __factory.generate_node("fano_graph")
    # Create nodes
    node_names = ["0", "1", "2", "3", "4", "5", "6"]
    __nodes = []
    for n0 in node_names:
        __nodes.append(__factory.generate_node(n0, test_system))
    # Create edges
    __factory.connect_nodes(test_system, "e013", [__nodes[0], __nodes[1], __nodes[3]], EnumRelationDirection.BIDIRECTIONAL)
    __factory.connect_nodes(test_system, "e156", [__nodes[1], __nodes[5], __nodes[6]], EnumRelationDirection.BIDIRECTIONAL)
    __factory.connect_nodes(test_system, "e235", [__nodes[2], __nodes[3], __nodes[5]], EnumRelationDirection.BIDIRECTIONAL)
    __factory.connect_nodes(test_system, "e124", [__nodes[1], __nodes[2], __nodes[4]], EnumRelationDirection.BIDIRECTIONAL)
    __factory.connect_nodes(test_system, "e346", [__nodes[3], __nodes[4], __nodes[6]], EnumRelationDirection.BIDIRECTIONAL)
    __factory.connect_nodes(test_system, "e045", [__nodes[0], __nodes[4], __nodes[5]], EnumRelationDirection.BIDIRECTIONAL)
    __factory.connect_nodes(test_system, "e026", [__nodes[0], __nodes[2], __nodes[6]], EnumRelationDirection.BIDIRECTIONAL)
    return __nodes, __factory, test_system


#
# END SEGMENT: FANO GRAPH
#


#
# Segment: Multi-tree
#


def create_multitree():
    __clock = DummyClock()
    __factory = HypergraphFactory("test", __clock)
    test_system = __factory.generate_node("multitree")
    # Create nodes
    node_names = ["0", "1", "2", "3", "4", "5", "6"]
    __nodes = []
    for n0 in node_names:
        __nodes.append(__factory.generate_node(n0, test_system))
    # Create edges
    __factory.connect_2factor_edges(test_system, "e4_013", [__nodes[4]], [__nodes[0], __nodes[1], __nodes[3]],
                                    (EnumRelationDirection.INWARDS, EnumRelationDirection.OUTWARDS))
    __factory.connect_2factor_edges(test_system, "e2_156", [__nodes[2]], [__nodes[1], __nodes[5], __nodes[6]],
                                    (EnumRelationDirection.INWARDS, EnumRelationDirection.OUTWARDS))
    __factory.connect_2factor_edges(test_system, "e1_235", [__nodes[1]], [__nodes[2], __nodes[3], __nodes[5]],
                                    (EnumRelationDirection.INWARDS, EnumRelationDirection.OUTWARDS))
    __factory.connect_2factor_edges(test_system, "e6_124", [__nodes[6]], [__nodes[1], __nodes[2], __nodes[4]],
                                    (EnumRelationDirection.INWARDS, EnumRelationDirection.OUTWARDS))
    __factory.connect_2factor_edges(test_system, "e1_346", [__nodes[1]], [__nodes[3], __nodes[4], __nodes[6]],
                                    (EnumRelationDirection.INWARDS, EnumRelationDirection.OUTWARDS))
    __factory.connect_2factor_edges(test_system, "e3_045", [__nodes[3]], [__nodes[0], __nodes[4], __nodes[5]],
                                    (EnumRelationDirection.INWARDS, EnumRelationDirection.OUTWARDS))
    __factory.connect_2factor_edges(test_system, "e1_026", [__nodes[1]], [__nodes[0], __nodes[2], __nodes[6]],
                                    (EnumRelationDirection.INWARDS, EnumRelationDirection.OUTWARDS))
    return __nodes, __factory, test_system

#
# END SEGMENT: Simple Multi-tree
#

#
# Segment: simple tree
#

def create_simple_tree():
    __clock = DummyClock()
    __factory = HypergraphFactory("test", __clock)
    test_system = __factory.generate_node("testtree")
    # Create nodes
    node_names = ["0", "1", "2"]
    __nodes = []
    for n0 in node_names:
        __nodes.append(__factory.generate_node(n0, test_system))
    # Create edges
    __factory.connect_dir_edges(test_system, "e0_1", [__nodes[0]], [__nodes[1]])
    __factory.connect_dir_edges(test_system, "e0_2", [__nodes[0]], [__nodes[2]])
    return __nodes, __factory, test_system
