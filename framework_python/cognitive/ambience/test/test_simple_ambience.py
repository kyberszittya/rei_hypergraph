from presentation.graphviz.graphviz_mapping import create_graph_view
from simulation.sdf.sdf_generator import load_from_description


def test_example_robotcar_w_ambient():
    sys, _ = load_from_description("../examples/example_robotcar_ambient.cogni")
    create_graph_view(sys)
