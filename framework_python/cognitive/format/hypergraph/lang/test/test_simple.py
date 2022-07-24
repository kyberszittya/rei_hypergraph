from cognitive.format.hypergraph.channels.tensor_channel import CognitiveArbiter, TensorCognitiveIcon, CognitiveChannel, \
    HypergraphTensorTransformation
from cognitive.format.hypergraph.lang.mapping.cogni_lang_mapping import load_from_description
from cognitive.format.hypergraph.lang.mapping.graphviz_mapping import create_graph_view


def test_example_kinematic_loop():
    sys, _ = load_from_description("../examples/example_kinematic_loop.cogni")
    create_graph_view(sys)


def test_pendulum():
    sys, _ = load_from_description("../examples/pendulum.cogni")
    create_graph_view(sys)


def test_pendulum_2link():
    sys, channel = load_from_description("../examples/two_link_pendulum.cogni")
    create_graph_view(sys)


def test_simplebot():
    sys, channel = load_from_description("../examples/example_robotcar.cogni")
    create_graph_view(sys)


def test_simplebot_entropy():
    sys, channel = load_from_description("../examples/example_robotcar.cogni")
    create_graph_view(sys)
    sys = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, sys)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, sys.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    tensor = ch.encode([sys])
    print(tensor)

