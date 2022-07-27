from cognitive.format.hypergraph.channels.tensor_channel import CognitiveArbiter, TensorCognitiveIcon, CognitiveChannel, \
    HypergraphTensorTransformation, HypergraphCoordinateObject
from cognitive.format.hypergraph.lang.mapping.cogni_lang_mapping import load_from_description
from cognitive.format.hypergraph.lang.mapping.graphviz_mapping import create_graph_view
from cognitive.format.hypergraph.laplacian.graph_tensor_operations import graph_upper_bound_entropy_vector

from cbor2 import dumps

def test_simplebot_entropy_coo():
    sys, channel = load_from_description("../examples/example_robotcar.cogni")
    create_graph_view(sys)
    arbiter = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, arbiter)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, arbiter.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    tensor = ch.encode([sys])
    #print(tensor)
    coo_icon = TensorCognitiveIcon("coo", 0)
    coo_ch = HypergraphCoordinateObject("coo1", 0, arbiter.domain, channel, coo_icon)
    coo_ch.encode([sys])
    #print(graph_upper_bound_entropy_vector(tensor))
    data = dumps([list(coo_ch.homomorphism_node.keys()),
                  list(coo_ch.homomorphism_edge.keys()),
                  coo_ch.intermediate_tensor.tolist()
                  ])
    print(len(data))

