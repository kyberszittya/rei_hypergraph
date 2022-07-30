from rei.cognitive.channels.channel_base_definitions import CognitiveArbiter, CognitiveChannel
from rei.cognitive.channels.cognitive_dendrite import HypergraphTensorTransformation, HypergraphCoordinateObject
from rei.cognitive.channels.cognitive_icons import TensorCognitiveIcon
from rei.presentation.graphviz.graphviz_mapping import create_graph_view
from rei.simulation.sdf.sdf_generator import load_from_description

__OUTPUT_DIR: str = "output"


def test_example_kinematic_loop():
    sys, _, icon = list(load_from_description("examples/example_kinematic_loop.cogni", __OUTPUT_DIR))[0]
    icon.view()
    create_graph_view(sys, "output")


def test_pendulum():
    sys, _, icon = list(load_from_description("examples/pendulum.cogni", __OUTPUT_DIR))[0]
    icon.view()
    create_graph_view(sys, "output")


def test_pendulum_2link():
    sys, channel, icon = list(load_from_description("examples/two_link_pendulum.cogni", __OUTPUT_DIR))[0]
    icon.view()
    create_graph_view(sys, "output")


__ROBOTCAR_FILENAME: str = "examples/example_robotcar.cogni"


def test_simplebot():
    sys, channel, icon = list(load_from_description(__ROBOTCAR_FILENAME, __OUTPUT_DIR))[0]
    icon.view()
    create_graph_view(sys, "output")


def test_simplebot_entropy():
    sys, channel, file_icon = list(load_from_description(__ROBOTCAR_FILENAME, __OUTPUT_DIR))[0]
    create_graph_view(sys, "output")
    #
    file_icon.view()
    #
    arbiter = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, arbiter)
    tensor_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, arbiter.domain, channel, tensor_icon)
    channel.add_connection(ch, 0, tensor_icon)
    file_icon.view()
    ch.encode([sys])


def test_simplebot_entropy_coo():
    sys, channel, file_icon = list(load_from_description(__ROBOTCAR_FILENAME, __OUTPUT_DIR))[0]
    create_graph_view(sys, "output")
    #
    file_icon.view()
    #
    arbiter = CognitiveArbiter(name="sys", timestamp=0)
    channel = CognitiveChannel("channel_01", 0, arbiter)
    view_icon = TensorCognitiveIcon("out", 0)
    ch = HypergraphTensorTransformation("dendrite1", 0, arbiter.domain, channel, view_icon)
    channel.add_connection(ch, 0, view_icon)
    ch.encode([sys])
    coo_icon = TensorCognitiveIcon("coo", 0)
    coo_ch = HypergraphCoordinateObject("coo1", 0, arbiter.domain, channel, coo_icon)
    coo_ch.encode([sys])
