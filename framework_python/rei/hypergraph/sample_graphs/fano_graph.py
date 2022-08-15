from rei.factories.foundation_factory import HypergraphFactory
from rei.foundations.clock import MetaClock


def create_fano_graph(context_name: str, clock: MetaClock):
    __factory = HypergraphFactory(context_name, clock)
    __n0 = __factory.generate_node(context_name)
    __node_list = __factory.generate_list_nodes([str(x) for x in range(7)], __n0)
    # Check whether anyhow the UUIDs are not equal
    __uuid_set = set()
    for n in __node_list:
        assert n.uuid not in __uuid_set
        __uuid_set.add(n.uuid)
    # Connect the set of nodes
    __edges = [__factory.connect_nodes(__n0, "e012", [__node_list[0], __node_list[1], __node_list[2]]),
               __factory.connect_nodes(__n0, "e234", [__node_list[2], __node_list[3], __node_list[4]]),
               __factory.connect_nodes(__n0, "e146", [__node_list[1], __node_list[4], __node_list[6]]),
               __factory.connect_nodes(__n0, "e036", [__node_list[0], __node_list[3], __node_list[6]]),
               __factory.connect_nodes(__n0, "e256", [__node_list[2], __node_list[5], __node_list[6]]),
               __factory.connect_nodes(__n0, "e135", [__node_list[1], __node_list[3], __node_list[5]]),
               __factory.connect_nodes(__n0, "e045", [__node_list[0], __node_list[4], __node_list[5]])]
    return __factory, __n0, __node_list, __edges