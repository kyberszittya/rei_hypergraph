from rei.format.semantics.CognitiveEntity import AmbientNodeInterface, CognitiveEntity, AmbiencePortCommunication, \
    AmbiencePort
from rei.hypergraph.base_elements import HypergraphEdge, HypergraphNode
from rei.hypergraph.common_definitions import EnumRelationDirection


def extract_ambient_data_from_node_interface(root_item: CognitiveEntity, r: AmbientNodeInterface):
    ambience_text_data = {}

    edge: HypergraphEdge = r.parent
    class_name = ''.join([x.capitalize() for x in r.id_name.split('_')])
    ambience_text_data["class_name"] = class_name
    ambience_text_data["pub_ambience_ports"] = []
    ambience_text_data["sub_ambience_ports"] = []
    file_name = '_'.join([root_item.id_name.upper(), r.id_name.upper()])
    ambience_text_data["file_name"] = file_name
    items = filter(lambda x: x.has_item(lambda x: isinstance(x, AmbiencePortCommunication)), edge.sub_relations)
    for i in items:
        n: HypergraphNode = i.endpoint
        port: AmbiencePort = next(n.get_element_by_id_name(n.id_name))
        msg_type = port.get_id_name_from_attribute("msgtype").replace('"', '').strip()
        msg_type = msg_type.split("/")
        # Class name
        port_name = ''.join([x.capitalize() for x in port.get_id_name_from_attribute("name").split('_')])
        match i.direction:
            case EnumRelationDirection.OUTWARDS:
                ambience_text_data["pub_ambience_ports"].append((port_name, "::".join(msg_type),
                                                                 port.get_id_name_from_attribute("topicname")))
            case EnumRelationDirection.INWARDS:
                ambience_text_data["sub_ambience_ports"].append((port_name, "::".join(msg_type),
                                                                 port.get_id_name_from_attribute("topicname")))
    return ambience_text_data