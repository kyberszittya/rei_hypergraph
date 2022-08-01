from rei.cognitive.ambience.elements.definitive_elements import AmbienceEdge, EnumCommunicationType, \
    AmbienceCommunicationConnection
from rei.cognitive.format.basicelements.concepts.network.base_definitions import EnumRelationDirection
from rei.cognitive.format.hypergraph.foundations.hypergraph_elements import HypergraphNode
from rei.cognitive.format.hypergraph.foundations.hypergraph_operators import retrieve_part_hypergraph_node


def connect_ambience_to_port(context: HypergraphNode, timestamp: int, ambience: AmbienceEdge,
                             comm_type: EnumCommunicationType,
                             target_qualified_name: str, direction: EnumRelationDirection):
    #ambience.communication_type = comm_type
    target_name: str = '/'.join([context.progenitor_registry.qualified_name, target_qualified_name])
    res_target = list(retrieve_part_hypergraph_node(context,target_name))
    if len(res_target) != 0:
        target_node = res_target[0]
        ambience.connect(res_target[0], 1, 0, direction)
        conn = AmbienceCommunicationConnection('/'.join([ambience.id_name, target_node.id_name]), timestamp,
                                               comm_type=comm_type, domain=ambience.domain, direction=direction)
        ambience.add_connection(conn, 0, target_node, direction)