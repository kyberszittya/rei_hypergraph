from cognitive.channels.channel_base_definitions import CognitiveArbiter, CognitiveChannel
from cognitive.channels.cognitive_dendrite import HypergraphTensorTransformation, HypergraphCoordinateObject
from cognitive.channels.cognitive_icons import TensorCognitiveIcon, ByteBufferCognitiveIcon
from presentation.graphviz.graphviz_mapping import create_graph_view
from simulation.sdf.sdf_generator import load_from_description


def test_simplebot_entropy_coo():
    sys, channel, icon = load_from_description("../examples/example_robotcar.cogni", output_dir="../../output/encoding")
    create_graph_view(sys, output_directory="output")
    arbiter = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, arbiter)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, arbiter.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    coo_icon = TensorCognitiveIcon("coo", 0)
    coo_ch = HypergraphCoordinateObject("coo1", 0, arbiter.domain, channel, coo_icon)
    byte_stream_icon = ByteBufferCognitiveIcon("byte_out", 0)
    channel.add_connection(coo_ch, 0, byte_stream_icon)
    coo_ch.encode([sys])
    print(byte_stream_icon.view())



