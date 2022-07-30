from rei.presentation.graphviz.graphviz_mapping import create_graph_view
from rei.simulation.sdf.sdf_generator import load_from_description


__FILE_ROBOTCAR_W_AMBIENT = "examples/example_robotcar_ambient.cogni"


def test_example_robotcar_w_ambient():
    sys, _, icon = list(load_from_description(__FILE_ROBOTCAR_W_AMBIENT, output_dir="output"))[0]
    create_graph_view(sys, "output")
