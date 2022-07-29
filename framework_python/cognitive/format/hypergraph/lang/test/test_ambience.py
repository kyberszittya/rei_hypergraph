from cognitive.format.hypergraph.lang.mapping.cogni_lang_mapping import load_from_description
from cognitive.format.hypergraph.lang.mapping.graphviz_mapping import create_graph_view


def test_example_robotcar_w_ambient():
    sys, _ = load_from_description("../examples/example_robotcar_ambient.cogni")
    create_graph_view(sys)
