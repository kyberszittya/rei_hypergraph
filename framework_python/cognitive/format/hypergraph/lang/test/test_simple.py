from cognitive.format.hypergraph.lang.mapping.cogni_lang_mapping import load_from_description
from cognitive.format.hypergraph.lang.mapping.graphviz_mapping import create_graph_view


def test_example_kinematic_loop():
    sys, _ = load_from_description("D:\\Haizu\\robotics_ws\\cogni_ws\\rei_ws\\rei\\framework_python\\cognitive\\format\\hypergraph\\lang\\examples\\example_kinematic_loop.cogni")
    create_graph_view(sys)


def test_pendulum():
    sys, _ = load_from_description("D:\\Haizu\\robotics_ws\\cogni_ws\\rei_ws\\rei\\framework_python\\cognitive\\format\\hypergraph\\lang\\examples\\pendulum.cogni")
    create_graph_view(sys)


def test_pendulum_2link():
    sys, channel = load_from_description("D:\\Haizu\\robotics_ws\\cogni_ws\\rei_ws\\rei\\framework_python\\cognitive\\format\\hypergraph\\lang\\examples\\two_link_pendulum.cogni")
    create_graph_view(sys)


def test_simplebot():
    sys, channel = load_from_description("D:\\Haizu\\robotics_ws\\cogni_ws\\rei_ws\\rei\\framework_python\\cognitive\\format\\hypergraph\\lang\\examples\\example_robotcar.cogni")
    create_graph_view(sys)
